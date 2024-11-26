from django.db import connection
from django.shortcuts import render, redirect


def admin_books_list(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT b.id, b.title, b.publication_year, a.name as author_name, p.name as publisher_name 
            FROM books b
            JOIN authors a ON b.author_id = a.id
            JOIN publishers p ON b.publisher_id = p.id
        """)
        books = cursor.fetchall()

    return render(request, 'admin/books_list.html', {'books': books})


def admin_delete_book(request, book_id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM bookgenres WHERE book_id = %s", [book_id])
        cursor.execute("DELETE FROM books WHERE id = %s", [book_id])
    return redirect('admin_books_list')


def admin_genres_list(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, name, description FROM genres")
        genres = cursor.fetchall()

    return render(request, 'admin/genres_list.html', {'genres': genres})

def book_form_view(request, book_id=None):
    # Получаем список авторов, издательств и жанров
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, name FROM authors")
        authors = cursor.fetchall()

        cursor.execute("SELECT id, name FROM publishers")
        publishers = cursor.fetchall()

        cursor.execute("SELECT id, name FROM genres")
        genres = cursor.fetchall()

    # Если это редактирование книги, получаем данные о книге
    book = None
    book_genres = []
    if book_id:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, title, publication_year, description, pages, subscription_only, author_id, publisher_id 
                FROM books WHERE id = %s
            """, [book_id])
            book = cursor.fetchone()

            # Получаем связанные жанры
            cursor.execute("""
                SELECT genre_id FROM bookgenres WHERE book_id = %s
            """, [book_id])
            book_genres = [genre[0] for genre in cursor.fetchall()]

    if request.method == 'POST':
        title = request.POST['title']
        publication_year = request.POST['publication_year']
        author_id = request.POST['author']
        publisher_id = request.POST['publisher']
        description = request.POST['description']
        subscription_only = bool(request.POST.get('subscription_only', False))
        pages = request.POST['pages']
        selected_genres = request.POST.getlist('genres')

        if book_id:
            # Обновление книги
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE books 
                    SET title = %s, publication_year = %s, author_id = %s, publisher_id = %s, 
                        description = %s, subscription_only = %s, pages = %s 
                    WHERE id = %s
                """, [title, publication_year, author_id, publisher_id, description, subscription_only, pages, book_id])

                # Удаляем старые связи книги с жанрами
                cursor.execute("DELETE FROM bookgenres WHERE book_id = %s", [book_id])

                # Добавляем новые связи с жанрами
                for genre_id in selected_genres:
                    cursor.execute("""
                        INSERT INTO bookgenres (book_id, genre_id) 
                        VALUES (%s, %s)
                    """, [book_id, genre_id])
        else:
            # Добавление новой книги
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO books (title, publication_year, author_id, publisher_id, description, subscription_only, pages) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id
                """, [title, publication_year, author_id, publisher_id, description, subscription_only, pages])
                new_book_id = cursor.fetchone()[0]

                # Добавляем связи книги с жанрами
                for genre_id in selected_genres:
                    cursor.execute("""
                        INSERT INTO bookgenres (book_id, genre_id) 
                        VALUES (%s, %s)
                    """, [new_book_id, genre_id])

        return redirect('admin_books_list')

    return render(request, 'admin/book_form.html', {
        'book': book,
        'authors': authors,
        'publishers': publishers,
        'genres': genres,
        'book_genres': book_genres,
    })