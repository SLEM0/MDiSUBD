from django.db import connection
from django.shortcuts import render

def book_catalog_view(request):
    # Получаем параметры для сортировки и фильтрации из запроса
    sort_by = request.GET.get('sort', 'title')  # По умолчанию сортировка по названию
    without_subscription = request.GET.get('without_subscription')  # Чекбокс "Без подписки"
    authors = request.GET.getlist('author')  # Выбранные авторы
    publishers = request.GET.getlist('publisher')  # Выбранные издательства
    genres = request.GET.getlist('genre')  # Выбранные жанры
    min_year = request.GET.get('min_year')  # Минимальный год публикации
    max_year = request.GET.get('max_year')  # Максимальный год публикации
    min_pages = request.GET.get('min_pages')  # Минимальное количество страниц
    max_pages = request.GET.get('max_pages')  # Максимальное количество страниц

    # Получаем список авторов
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, name FROM authors")
        authors_list = cursor.fetchall()

    # Получаем список издательств
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, name FROM publishers")
        publishers_list = cursor.fetchall()

    # Получаем список жанров
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, name FROM genres")
        genres_list = cursor.fetchall()

    # Строим базовый SQL-запрос для книг
    query = """
        SELECT DISTINCT b.id, b.title, b.publication_year, b.description, b.pages
        FROM books b
        LEFT JOIN bookgenres bg ON b.id = bg.book_id
        LEFT JOIN genres g ON bg.genre_id = g.id
    """
    conditions = []  # Условия для фильтрации

    # Фильтр "Без подписки"
    if without_subscription:
        conditions.append("b.subscription_only = FALSE")

    # Фильтр по авторам
    if authors:
        author_ids = ','.join(authors)
        conditions.append(f"b.author_id IN ({author_ids})")

    # Фильтр по издательствам
    if publishers:
        publisher_ids = ','.join(publishers)
        conditions.append(f"b.publisher_id IN ({publisher_ids})")

    # Фильтр по жанрам
    if genres:
        genre_ids = ','.join(genres)
        conditions.append(f"bg.genre_id IN ({genre_ids})")

    # Фильтр по году публикации
    if min_year:
        conditions.append(f"b.publication_year >= {min_year}")
    if max_year:
        conditions.append(f"b.publication_year <= {max_year}")

    # Фильтр по количеству страниц
    if min_pages:
        conditions.append(f"b.pages >= {min_pages}")
    if max_pages:
        conditions.append(f"b.pages <= {max_pages}")

    # Добавляем условия фильтрации в запрос
    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    # Определяем порядок сортировки
    if sort_by == 'year':
        query += " ORDER BY b.publication_year"
    elif sort_by == 'pages':
        query += " ORDER BY b.pages"
    else:  # Default sorting by title
        query += " ORDER BY b.title"

    # Выполняем SQL-запрос для получения книг
    with connection.cursor() as cursor:
        cursor.execute(query)
        books = cursor.fetchall()

    # Формируем список словарей для передачи в шаблон
    book_list = []
    for book in books:
        book_list.append({
            'id': book[0],
            'title': book[1],
            'publication_year': book[2],
            'description': book[3],
            'pages': book[4],
        })

    # Формируем список авторов, издательств и жанров
    authors_data = [{'id': author[0], 'name': author[1]} for author in authors_list]
    publishers_data = [{'id': publisher[0], 'name': publisher[1]} for publisher in publishers_list]
    genres_data = [{'id': genre[0], 'name': genre[1]} for genre in genres_list]

    # Подготовка списков для выбранных авторов, издательств и жанров
    selected_authors = set(authors)  # Используем множество для проверки
    selected_publishers = set(publishers)
    selected_genres = set(genres)

    is_authenticated = 'user_id' in request.session

    # Передаем список книг, авторов, издательств и жанров в шаблон
    context = {
        'books': book_list,
        'sort_by': sort_by,
        'without_subscription': without_subscription,
        'authors': authors_data,
        'publishers': publishers_data,
        'genres': genres_data,
        'min_year': min_year,
        'max_year': max_year,
        'min_pages': min_pages,
        'max_pages': max_pages,
        'selected_authors': selected_authors,
        'selected_publishers': selected_publishers,
        'selected_genres': selected_genres,
        'is_authenticated': is_authenticated,
    }
    
    return render(request, 'book_catalog.html', context)


def book_detail_view(request, book_id):
    user_id = request.session.get('user_id')  # Получаем текущего пользователя
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT b.id, b.title, b.publication_year, b.description, b.pages, b.average_rating,
                   a.name as author_name, p.name as publisher_name
            FROM books b
            JOIN authors a ON b.author_id = a.id
            JOIN publishers p ON b.publisher_id = p.id
            WHERE b.id = %s
        """, [book_id])
        book = cursor.fetchone()

    # Получаем жанры книги
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT g.name 
            FROM genres g
            JOIN bookgenres bg ON g.id = bg.genre_id
            WHERE bg.book_id = %s
        """, [book_id])
        genres = cursor.fetchall()

    # Получаем отзывы на книгу
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT r.rating, r.comment, r.created_at, u.username 
            FROM reviews r
            JOIN users u ON r.user_id = u.id
            WHERE r.book_id = %s
            ORDER BY r.created_at DESC
        """, [book_id])
        reviews = cursor.fetchall()

    # Проверяем, есть ли книга в "Мои чтения" или "Читать позже"
    in_current_reads = False
    in_read_later = False

    if user_id:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*) FROM currentreads WHERE user_id = %s AND book_id = %s
            """, [user_id, book_id])
            in_current_reads = cursor.fetchone()[0] > 0

            cursor.execute("""
                SELECT COUNT(*) FROM readlater WHERE user_id = %s AND book_id = %s
            """, [user_id, book_id])
            in_read_later = cursor.fetchone()[0] > 0

    book_data = {
        'id': book[0],
        'title': book[1],
        'publication_year': book[2],
        'description': book[3],
        'pages': book[4],
        'average_rating': book[5],
        'author_name': book[6],
        'publisher_name': book[7],
        'genres': [genre[0] for genre in genres],
    }

    return render(request, 'book_detail.html', {
        'book': book_data,
        'reviews': reviews,
        'in_current_reads': in_current_reads,
        'in_read_later': in_read_later,
    })