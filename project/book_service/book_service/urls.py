from django.contrib import admin
from django.urls import path
from main.views.admin.authors_views import *
from main.views.admin.books_views import *
from main.views.admin.genres_views import *
from main.views.admin.publishers_views import *
from main.views.admin.statistics_views import *
from main.views.admin.users_views import *
from main.views.auth_views import *
from main.views.book.actions_views import *
from main.views.book.catalog_views import *
from main.views.book.user_books_views import *
from main.views.user_views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', book_catalog_view, name='book_catalog'),
    path('profile/', profile_view, name='profile'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('my_readings/', my_readings_view, name='my_readings'),
    path('read_later/', read_later_view, name='read_later'),
    path('users/create/', admin_create_user_view, name='admin_create_user'),
    path('admin_statistics/', admin_statistics_view, name='admin_statistics'),
    path('user_statistics/', user_statistics_view, name='user_statistics'),
    path('delete_from_my_readings/<int:book_id>/', delete_from_my_readings, name='delete_from_my_readings'),
    path('delete_from_read_later/<int:book_id>/', delete_from_read_later, name='delete_from_read_later'),
    path('subscription/', user_subscription_view, name='user_subscription'),
    path('subscription/create/<int:months>/', create_subscription, name='create_subscription'),
    path('add_review/<int:book_id>/', add_review_view, name='add_review'),
    path('add_to_my_readings/<int:book_id>/', add_to_my_readings, name='add_to_my_readings'),
    path('add_to_read_later/<int:book_id>/', add_to_read_later, name='add_to_read_later'),
    path('read_book/<int:book_id>/', read_book_view, name='read_book'),
    path('move_to_my_readings/<int:book_id>/', move_to_my_readings_view, name='move_to_my_readings'),
    path('book/<int:book_id>/', book_detail_view, name='book_detail'),
    # CRUD для книг
    path('books/', admin_books_list, name='admin_books_list'),
    path('books/add/', book_form_view, name='admin_add_book'),
    path('books/edit/<int:book_id>/', book_form_view, name='admin_edit_book'),
    path('books/delete/<int:book_id>/', admin_delete_book, name='admin_delete_book'),
    # CRUD для жанров
    path('genres/', admin_genres_list, name='admin_genres_list'),
    path('genres/add/', admin_add_genre, name='admin_add_genre'),
    path('genres/edit/<int:genre_id>/', admin_edit_genre, name='admin_edit_genre'),
    path('genres/delete/<int:genre_id>/', admin_delete_genre, name='admin_delete_genre'),
    # CRUD для авторов
    path('authors/', admin_authors_list, name='admin_authors_list'),
    path('authors/add/', admin_add_author, name='admin_add_author'),
    path('authors/edit/<int:author_id>/', admin_edit_author, name='admin_edit_author'),
    path('authors/delete/<int:author_id>/', admin_delete_author, name='admin_delete_author'),
    # CRUD для издательств
    path('publishers/', admin_publishers_list, name='admin_publishers_list'),
    path('publishers/add/', admin_add_publisher, name='admin_add_publisher'),
    path('publishers/edit/<int:publisher_id>/', admin_edit_publisher, name='admin_edit_publisher'),
    path('publishers/delete/<int:publisher_id>/', admin_delete_publisher, name='admin_delete_publisher'),
]
