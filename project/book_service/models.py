from django.db import models


class Actionlogs(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING)
    action_type = models.CharField(max_length=255)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'actionlogs'


class Authors(models.Model):
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)
    biography = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'authors'


class Bookgenres(models.Model):
    book = models.OneToOneField('Books', models.DO_NOTHING, primary_key=True)  # The composite primary key (book_id, genre_id) found, that is not supported. The first column is selected.
    genre = models.ForeignKey('Genres', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'bookgenres'
        unique_together = (('book', 'genre'),)


class Books(models.Model):
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Authors, models.DO_NOTHING)
    publisher = models.ForeignKey('Publishers', models.DO_NOTHING)
    description = models.TextField(blank=True, null=True)
    subscription_only = models.BooleanField(blank=True, null=True)
    pages = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'books'


class Currentreads(models.Model):
    user = models.OneToOneField('Users', models.DO_NOTHING, primary_key=True)  # The composite primary key (user_id, book_id) found, that is not supported. The first column is selected.
    book = models.ForeignKey(Books, models.DO_NOTHING)
    added_at = models.DateTimeField(blank=True, null=True)
    pages_read = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'currentreads'
        unique_together = (('user', 'book'),)


class Genres(models.Model):
    name = models.CharField(unique=True, max_length=50)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'genres'


class Publishers(models.Model):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=100, blank=True, null=True)
    founded_year = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'publishers'


class Readlater(models.Model):
    user = models.OneToOneField('Users', models.DO_NOTHING, primary_key=True)  # The composite primary key (user_id, book_id) found, that is not supported. The first column is selected.
    book = models.ForeignKey(Books, models.DO_NOTHING)
    added_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'readlater'
        unique_together = (('user', 'book'),)


class Reviews(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING)
    book = models.ForeignKey(Books, models.DO_NOTHING)
    rating = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'reviews'


class Subscriptions(models.Model):
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'subscriptions'


class Users(models.Model):
    username = models.CharField(unique=True, max_length=50)
    password = models.CharField(max_length=255)
    email = models.CharField(unique=True, max_length=100)
    is_superuser = models.BooleanField()
    created_at = models.DateTimeField(blank=True, null=True)
    subscription = models.ForeignKey(Subscriptions, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'
