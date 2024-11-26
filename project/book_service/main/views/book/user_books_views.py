from django.db import connection
from django.shortcuts import render, redirect
from django.contrib import messages


def my_readings_view(request):
    user_id = request.session.get('user_id')
    
    if not user_id:
        return redirect('login')

    # Прямой SQL-запрос для получения книг, которые пользователь читает
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT b.title, b.pages, cr.pages_read, cr.added_at, b.id
            FROM currentreads cr
            JOIN books b ON cr.book_id = b.id
            WHERE cr.user_id = %s
        """, [user_id])
        current_readings = cursor.fetchall()

    return render(request, 'my_readings.html', {'current_readings': current_readings})


def read_later_view(request):
    user_id = request.session.get('user_id')
    
    if not user_id:
        return redirect('login')

    with connection.cursor() as cursor:
        # Выполняем запрос на получение книг из списка "Читать позже" для текущего пользователя
        cursor.execute("""
            SELECT b.id, b.title
            FROM readlater rl
            JOIN books b ON rl.book_id = b.id
            WHERE rl.user_id = %s
        """, [user_id])
        read_later_books = cursor.fetchall()

    # Передаем данные в шаблон
    return render(request, 'read_later.html', {
        'read_later_books': read_later_books
    })


def add_review_view(request, book_id):
    user_id = request.session.get('user_id')
    
    if not user_id:
        return redirect('login')  # Перенаправляем на страницу входа, если пользователь не авторизован

    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        # Проверяем, что пользователь уже не оставлял отзыв на эту книгу
        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM reviews WHERE user_id = %s AND book_id = %s", [user_id, book_id])
            existing_review = cursor.fetchone()

            if existing_review:
                messages.error(request, 'Вы уже оставляли отзыв на эту книгу.')
                return redirect('my_readings')

            # Добавляем новый отзыв
            cursor.execute("""
                INSERT INTO reviews (user_id, book_id, rating, comment, created_at)
                VALUES (%s, %s, %s, %s, NOW())
            """, [user_id, book_id, rating, comment])

        messages.success(request, 'Отзыв успешно добавлен!')
        return redirect('my_readings')

    return render(request, 'add_review.html', {'book_id': book_id})