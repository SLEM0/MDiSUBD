from django.db import connection
from django.shortcuts import render, redirect


def admin_publishers_list(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, name, country, founded_year FROM publishers")
        publishers = cursor.fetchall()

    return render(request, 'admin/publishers_list.html', {'publishers': publishers})


def admin_add_publisher(request):
    if request.method == 'POST':
        name = request.POST['name']
        country = request.POST.get('country', '')
        founded_year = request.POST.get('founded_year', None)

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO publishers (name, country, founded_year)
                VALUES (%s, %s, %s)
            """, [name, country, founded_year])

        return redirect('admin_publishers_list')

    return render(request, 'admin/publisher_form.html')


def admin_edit_publisher(request, publisher_id):
    if request.method == 'POST':
        name = request.POST['name']
        country = request.POST.get('country', '')
        founded_year = request.POST.get('founded_year', None)

        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE publishers
                SET name = %s, country = %s, founded_year = %s
                WHERE id = %s
            """, [name, country, founded_year, publisher_id])

        return redirect('admin_publishers_list')

    # Получаем данные издательства
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, name, country, founded_year
            FROM publishers
            WHERE id = %s
        """, [publisher_id])
        publisher = cursor.fetchone()

    return render(request, 'admin/publisher_form.html', {'publisher': publisher})


def admin_delete_publisher(request, publisher_id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM publishers WHERE id = %s", [publisher_id])
    return redirect('admin_publishers_list')