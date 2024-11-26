from django.db import connection
from django.shortcuts import render, redirect


def admin_add_genre(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST.get('description', '')

        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO genres (name, description) VALUES (%s, %s)", [name, description])

        return redirect('admin_genres_list')

    return render(request, 'admin/genre_form.html')


def admin_edit_genre(request, genre_id):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST.get('description', '')

        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE genres
                SET name = %s, description = %s
                WHERE id = %s
            """, [name, description, genre_id])

        return redirect('admin_genres_list')

    # Получаем жанр для редактирования
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, name, description FROM genres WHERE id = %s", [genre_id])
        genre = cursor.fetchone()

    return render(request, 'admin/genre_form.html', {'genre': genre})


def admin_delete_genre(request, genre_id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM bookgenres WHERE genre_id = %s", [genre_id])
        cursor.execute("DELETE FROM genres WHERE id = %s", [genre_id])
    return redirect('admin_genres_list')