from django.db import connection
from django.shortcuts import render, redirect
from django.contrib import messages
from main.forms import UserCreationForm


def admin_create_user_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            is_superuser = form.cleaned_data['is_superuser']

            # Вставляем нового пользователя в базу данных
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO users (username, email, password, is_superuser, created_at)
                    VALUES (%s, %s, %s, %s, NOW())
                """, [username, email, password, is_superuser])

            messages.success(request, 'Пользователь успешно создан!')
            return redirect('profile')  # Перенаправляем на список пользователей
    else:
        form = UserCreationForm()

    return render(request, 'admin/admin_create_user.html', {'form': form})