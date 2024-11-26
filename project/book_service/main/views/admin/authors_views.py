from django.db import connection
from django.shortcuts import render, redirect


def admin_authors_list(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, name, date_of_birth, biography FROM authors")
        authors = cursor.fetchall()

    return render(request, 'admin/authors_list.html', {'authors': authors})


def admin_add_author(request):
    if request.method == 'POST':
        name = request.POST['name']
        date_of_birth = request.POST.get('date_of_birth', None)
        biography = request.POST.get('biography', '')

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO authors (name, date_of_birth, biography)
                VALUES (%s, %s, %s)
            """, [name, date_of_birth, biography])

        return redirect('admin_authors_list')

    return render(request, 'admin/author_form.html')


def admin_edit_author(request, author_id):
    if request.method == 'POST':
        name = request.POST['name']
        date_of_birth = request.POST.get('date_of_birth', None)
        biography = request.POST.get('biography', '')

        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE authors
                SET name = %s, date_of_birth = %s, biography = %s
                WHERE id = %s
            """, [name, date_of_birth, biography, author_id])

        return redirect('admin_authors_list')

    # Получаем данные об авторе
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, name, date_of_birth, biography
            FROM authors
            WHERE id = %s
        """, [author_id])
        author = cursor.fetchone()

    return render(request, 'admin/author_form.html', {'author': author})


def admin_delete_author(request, author_id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM authors WHERE id = %s", [author_id])
    return redirect('admin_authors_list')