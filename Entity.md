# Структура базы данных

## 1. Пользователь

**Таблица:** `Users`  
**Поля:**
- `id` (INT, PK, AUTO_INCREMENT) — уникальный идентификатор пользователя.
- `username` (VARCHAR(50), UNIQUE, NOT NULL) — логин пользователя.
- `password` (VARCHAR(255), NOT NULL) — пароль.
- `email` (VARCHAR(100), UNIQUE, NOT NULL) — электронная почта.
- `is_superuser` (BOOLEAN, NOT NULL) — роль пользователя.
- `created_at` (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP) — дата регистрации.

**Связи:**
- `subscription_id` — связь с таблицей `Subscriptions` (один к одному).
- Один ко многим с таблицей `ActionLogs`.
- Один ко многим с таблицей `CurrentReads`.
- Один ко многим с таблицей `Reviews`.
- Один ко многим с таблицей `ReadLater`.
- Один к одному с таблицей `Subscriptions`.

---

## 2. Книга

**Таблица:** `Books`  
**Поля:**
- `id` (INT, PK, AUTO_INCREMENT) — уникальный идентификатор книги.
- `title` (VARCHAR(255), NOT NULL) — название книги.
- `publication_year` (YEAR, NOT NULL) — год публикации книги.
- `author_id` (INT, FK, NOT NULL) — идентификатор автора.
- `publisher_id` (INT, FK, NOT NULL) - идентификатор издательства.
- `description` (TEXT) — краткое описание книги.
- `subscription_only` (BOOLEAN, DEFAULT FALSE) — флаг, указывающий, доступна ли книга только по подписке

**Связи:**
- `author_id` — связь с таблицей `Authors` (многие к одному).
- `publisher_id` — связь с таблицей `Publishers` (многие к одному).
- Один ко многим с таблицей `Reviews`.
- Один ко многим с таблицей `ReadLater`.
- Один ко многим с таблицей `CurrentReads`.
- Многие ко многим с таблицей `Genres` через промежуточную таблицу `BookGenres`.

---

## 3. Автор

**Таблица:** `Authors`  
**Поля:**
- `id` (INT, PK, AUTO_INCREMENT) — уникальный идентификатор автора.
- `name` (VARCHAR(100), NOT NULL) — имя автора.
- `date_of_birth` (DATE, NULL) — дата рождения автора.
- `biography` (DATE) — биография автора.

**Связи:**
- Один ко многим с таблицей `Books`.

---

## 4. Жанр

**Таблица:** `Genres`  
**Поля:**
- `id` (INT, PK, AUTO_INCREMENT) — уникальный идентификатор жанра.
- `name` (VARCHAR(50), UNIQUE, NOT NULL) — название жанра (например, "Фантастика", "Детектив").
- `description` (TEXT) — описание жанра.

**Связи:**
- Многие ко многим с таблицей `Books` через промежуточную таблицу `BookGenres`.

---

## 5. Журнал действий

**Таблица:** `ActionLogs`  
**Поля:**
- `id` (INT, PK, AUTO_INCREMENT) — уникальный идентификатор записи в журнале.
- `user_id` (INT, FK, NOT NULL) — идентификатор пользователя, совершившего действие.
- `action_type` (VARCHAR(255), NOT NULL) — тип действия.
- `timestamp` (TIMESTAMP, NOT NULL) — дата и время совершения действия.

**Связи:**
- `user_id` — связь с таблицей `Users` (многие к одному).

---

## 6. Отзыв

**Таблица:** `Reviews`  
**Поля:**
- `id` (INT, PK, AUTO_INCREMENT) — уникальный идентификатор отзыва.
- `user_id` (INT, FK, NOT NULL) — идентификатор читателя, который оставил отзыв.
- `book_id` (INT, FK, NOT NULL) — идентификатор книги, к которой относится отзыв.
- `rating` (INT, NOT NULL, CHECK (rating >= 1 AND rating <= 5)) — оценка книги по шкале от 1 до 5.
- `comment` (TEXT) — текст отзыва о книге.
- `created_at` (TIMESTAMP, NOT NULL) — дата и время, когда был оставлен отзыв.

**Связи:**
- `user_id` — связь с таблицей `User` (многие к одному).
- `book_id` — связь с таблицей `Books` (многие к одному).

---

## 7. Подписка

**Таблица:** `Subscriptions`  
**Поля:**
- `id` (INT, PK, AUTO_INCREMENT) — уникальный идентификатор подписки.
- `user_id` (INT, FK, NOT NULL) — идентификатор пользователя.
- `start_date` (DATE, NOT NULL) — дата начала подписки.
- `end_date` (DATE) — дата окончания подписки.

**Связи:**
- Один к одному с таблицей `Users`.

---

### 8. Читать позже

**Таблица:** `ReadLater`
**Поля:**
- `user_id` (INT, FK, NOT NULL) — ссылка на пользователя.
- `book_id` (INT, FK, NOT NULL) — ссылка на книгу.
-``added_at` (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP) — дата добавления в "Читать позже".

**Связи:**
- `user_id` — связь с таблицей `User` (многие к одному).
- `book_id` — связь с таблицей `Books` (многие к одному).

---

### 9. Текущее чтение

**Таблица:** `CurrentReads`
**Поля:**
- `user_id` (INT, FK, NOT NULL) — ссылка на пользователя.
- `book_id` (INT, FK, NOT NULL) — ссылка на книгу.
- `added_at` (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP) — дата начала чтения.
- `pages_read` (INT, DEFAUTL 0)— количество страниц, прочитанных пользователем.

**Связи:**
- `user_id` — связь с таблицей `User` (многие к одному).
- `book_id` — связь с таблицей `Books` (многие к одному).

---

### 10. Издательство

**Таблица:** `Publishers`
**Поля:**
- `id` (INT, PK, AUTO_INCREMENT) — уникальный идентификатор издательства.
- `name` (VARCHAR(255), NOT NULL) — название издательства.
- `country` (VARCHAR(100), NULL) — страна, где находится издательство.
- `founded_year` (YEAR, NULL) — год основания издательства.

**Связи:**
- Один ко многим с таблицей `Books`.

---

## 11. Промежуточная таблица для связи "Книга - Жанр"

**Таблица:** `BookGenres`  
**Поля:**
- `book_id` (INT, FK, NOT NULL) — идентификатор книги.
- `genre_id` (INT, FK, NOT NULL) — идентификатор жанра.

**Связи:**
- Многие ко многим между таблицами `Books` и `Genres`.