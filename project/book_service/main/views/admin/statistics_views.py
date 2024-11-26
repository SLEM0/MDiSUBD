from django.db import connection
from django.shortcuts import render


def admin_statistics_view(request):
    with connection.cursor() as cursor:
        # Общее количество пользователей
        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]

        # Количество активных подписчиков
        cursor.execute("""
            SELECT COUNT(*)
            FROM users u
            JOIN subscriptions s ON u.subscription_id = s.id
            WHERE s.end_date > NOW()
        """)
        active_subscribers = cursor.fetchone()[0]

        # Самые популярные книги (по количеству добавлений в "Мои чтения")
        cursor.execute("""
            SELECT b.title, COUNT(cr.book_id) AS reading_count
            FROM books b
            JOIN currentreads cr ON b.id = cr.book_id
            GROUP BY b.title
            ORDER BY reading_count DESC
            LIMIT 5
        """)
        popular_books = cursor.fetchall()

        # Количество книг по жанрам
        cursor.execute("""
            SELECT g.name, COUNT(bg.book_id) AS book_count
            FROM genres g
            JOIN bookgenres bg ON g.id = bg.genre_id
            GROUP BY g.name
            ORDER BY book_count DESC
        """)
        books_by_genres = cursor.fetchall()

        # Топ-5 книг с наибольшим количеством отзывов
        cursor.execute("""
            SELECT b.title, COUNT(r.id) AS review_count
            FROM books b
            JOIN reviews r ON b.id = r.book_id
            GROUP BY b.title
            ORDER BY review_count DESC
            LIMIT 5
        """)
        top_books_by_reviews = cursor.fetchall()

        # Топ-5 самых активных пользователей
        cursor.execute("""
            SELECT u.username, COUNT(r.id) AS review_count
            FROM users u
            JOIN reviews r ON u.id = r.user_id
            GROUP BY u.username
            ORDER BY review_count DESC
            LIMIT 5
        """)
        top_active_users = cursor.fetchall()

    return render(request, 'admin/admin_statistics.html', {
        'total_users': total_users,
        'active_subscribers': active_subscribers,
        'popular_books': popular_books,
        'books_by_genres': books_by_genres,
        'top_books_by_reviews': top_books_by_reviews,
        'top_active_users': top_active_users,
    })