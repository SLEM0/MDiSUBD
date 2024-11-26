from django.db import connection
from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import timedelta

def profile_view(request):
    # Проверяем, авторизован ли пользователь
    user_id = request.session.get('user_id')
    
    if not user_id:
        # Если пользователь не авторизован, показываем ссылки на вход и регистрацию
        return render(request, 'profile.html', {
            'is_authenticated': False,
        })

    # Если пользователь авторизован, получаем его данные из базы
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT username, email, is_superuser
            FROM users
            WHERE id = %s
        """, [user_id])
        user = cursor.fetchone()

    if user:
        username, email, is_superuser = user
        return render(request, 'profile.html', {
            'is_authenticated': True,
            'username': username,
            'email': email,
            'is_superuser': is_superuser,
        })
    else:
        request.session.flush()
        return redirect('login')
    
def user_subscription_view(request):
    user_id = request.session.get('user_id')  # Получаем id пользователя из сессии
    if not user_id:
        return redirect('login')  # Если пользователь не авторизован, перенаправляем на страницу входа

    with connection.cursor() as cursor:
        # Проверяем, есть ли у пользователя подписка
        cursor.execute("""
            SELECT s.start_date, s.end_date 
            FROM subscriptions s
            JOIN users u ON u.subscription_id = s.id
            WHERE u.id = %s
        """, [user_id])
        subscription = cursor.fetchone()

    # Если подписка есть
    if subscription:
        subscription_info = {
            'start_date': subscription[0],
            'end_date': subscription[1] if subscription[1] else 'Не указано',
        }
    else:
        subscription_info = None

    return render(request, 'subscription_page.html', {
        'subscription_info': subscription_info,
    })

def user_statistics_view(request):
    user_id = request.session.get('user_id')  # Получаем ID текущего пользователя

    with connection.cursor() as cursor:
        # Количество книг в "Мои чтения"
        cursor.execute("SELECT COUNT(*) FROM currentreads WHERE user_id = %s", [user_id])
        current_reads_count = cursor.fetchone()[0]

        # Количество книг в "Читать позже"
        cursor.execute("SELECT COUNT(*) FROM readlater WHERE user_id = %s", [user_id])
        read_later_count = cursor.fetchone()[0]

        # Прогресс чтения (среднее значение по текущим книгам)
        cursor.execute("""
            SELECT b.title, cr.pages_read, b.pages
            FROM currentreads cr
            JOIN books b ON cr.book_id = b.id
            WHERE cr.user_id = %s
        """, [user_id])
        books = cursor.fetchall()

        book_progress = []
        for book in books:
            title, pages_read, total_pages = book
            if total_pages > 0:
                progress = (pages_read / total_pages) * 100
            else:
                progress = 0
            book_progress.append((title, pages_read, total_pages, progress))

        # Количество оставленных отзывов
        cursor.execute("SELECT COUNT(*) FROM reviews WHERE user_id = %s", [user_id])
        reviews_count = cursor.fetchone()[0]

        # Средний рейтинг, который пользователь поставил
        cursor.execute("SELECT AVG(r.rating) FROM reviews r WHERE r.user_id = %s", [user_id])
        average_rating = cursor.fetchone()[0]

        # Общее количество прочитанных страниц
        cursor.execute("SELECT SUM(cr.pages_read) FROM currentreads cr WHERE cr.user_id = %s", [user_id])
        total_pages_read = cursor.fetchone()[0] or 0  # Чтобы не было None, если ничего не прочитал

    return render(request, 'user_statistics.html', {
        'current_reads_count': current_reads_count,
        'read_later_count': read_later_count,
        'book_progress': book_progress,
        'reviews_count': reviews_count,
        'average_rating': average_rating,
        'total_pages_read': total_pages_read,
    })


# Обработка нажатия на одну из кнопок для создания подписки
def create_subscription(request, months):
    user_id = request.session.get('user_id')  # Получаем id пользователя из сессии
    if not user_id:
        return redirect('login')  # Если пользователь не авторизован, перенаправляем на страницу входа

    # Дата начала — текущая дата
    start_date = timezone.now().date()
    # Дата окончания — через выбранное количество месяцев
    end_date = start_date + timedelta(days=months * 30)

    # Создаем новую запись в таблице subscriptions
    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO subscriptions (start_date, end_date)
            VALUES (%s, %s) RETURNING id
        """, [start_date, end_date])
        subscription_id = cursor.fetchone()[0]

        # Привязываем новую подписку к пользователю
        cursor.execute("""
            UPDATE users SET subscription_id = %s WHERE id = %s
        """, [subscription_id, user_id])

    return redirect('user_subscription')