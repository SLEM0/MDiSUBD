from django.db import connection
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import DatabaseError


def add_to_my_readings(request, book_id):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')  # Если пользователь не авторизован

    try:
        with connection.cursor() as cursor:
            cursor.execute('CALL add_to_my_readings(%s, %s)', [user_id, book_id])  # Вызов хранимой процедуры
            messages.success(request, 'Книга добавлена в "Мои чтения".')

    except DatabaseError as e:
        messages.error(request, str(e))

    return redirect('book_detail', book_id=book_id)


def add_to_read_later(request, book_id):
    user_id = request.session.get('user_id')
    
    if not user_id:
        return redirect('login')  # Если пользователь не авторизован

    try:
        with connection.cursor() as cursor:
            cursor.execute('CALL add_to_readlater(%s, %s)', [user_id, book_id])  
            messages.success(request, 'Книга добавлена в "Читать позже".')

    except DatabaseError as e:
        messages.error(request, e)

    return redirect('book_detail', book_id=book_id)


def read_book_view(request, book_id):
    user_id = request.session.get('user_id')
    
    if not user_id:
        return redirect('login')

    # Получаем информацию о книге и прогрессе чтения
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT b.title, b.pages, cr.pages_read
            FROM books b
            JOIN currentreads cr ON cr.book_id = b.id
            WHERE cr.user_id = %s AND b.id = %s
        """, [user_id, book_id])
        book = cursor.fetchone()

    if not book:
        return redirect('my_readings')  # Если книга не найдена в чтениях

    title, total_pages, pages_read = book

    # Обработка кнопок для перехода на следующую/предыдущую страницу
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'next' and pages_read < total_pages:
            pages_read += 1
        elif action == 'prev' and pages_read > 0:
            pages_read -= 1

        # Обновляем прогресс чтения
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE currentreads
                SET pages_read = %s
                WHERE user_id = %s AND book_id = %s
            """, [pages_read, user_id, book_id])

    return render(request, 'read_book.html', {
        'title': title,
        'total_pages': total_pages,
        'pages_read': pages_read,
        'book_id': book_id
    })


def move_to_my_readings_view(request, book_id):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')

    try:
        print('try')
        with connection.cursor() as cursor:
            cursor.execute('CALL move_to_my_readings(%s, %s)', [user_id, book_id])  # Вызов хранимой процедуры
            print('good')
            messages.success(request, 'Книга добавлена в "Мои чтения".')

    except DatabaseError as e:
        messages.error(request, str(e))

    return redirect('read_later')


def delete_from_my_readings(request, book_id):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')

    with connection.cursor() as cursor:
        # Удаляем книгу из "Мои чтения"
        cursor.execute("""
            DELETE FROM currentreads WHERE user_id = %s AND book_id = %s
        """, [user_id, book_id])

    messages.success(request, 'Книга удалена из "Мои чтения".')
    return redirect('my_readings')


def delete_from_read_later(request, book_id):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')

    with connection.cursor() as cursor:
        # Удаляем книгу из "Мои чтения"
        cursor.execute("""
            DELETE FROM readlater WHERE user_id = %s AND book_id = %s
        """, [user_id, book_id])

    messages.success(request, 'Книга удалена из "Читать позже".')
    return redirect('read_later')