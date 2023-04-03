# API для проекта YaMDb

### О проекте
YaMDb позволяет оставлять отзывы на произведения (фильмы, книги, музыку и т.д.), а также оценивать их по 10-балльной шкале. Платформа содержит только информацию о развлекательном контенте, но не предоставляет прямой доступ к нему. 

Сервис использует следующие пользовательские роли:
- *Аноним* - может просматривать информацию о произведениях, читать отзывы и комментарии.
- *Аутентифицированный пользователь* (**user**) - может не только просматривать информацию, но и добавлять новые отзывы и комментарии, редактировать свои записи. Роль по умолчанию для новых пользователей.
- *Модератор* (**moderator**) - имеет доступ на управление не только своим, но и чужим контентом,  то есть может менять или удалять отзывы и комментарии других пользователей.
- *Администратор* (**admin**) - имеет все права модератора, а также может добавлять новые категории, жанры и произведения. Также назначает пользователям роли.
- *Суперпользователь Django*  - обладает всеми правами администратора, вне зависимости от указанной в профиле роли.

Для регистрации на платформе необходимо отправить POST-запрос, содержащий имя пользователя (**username**) и адрес электронной почты (**email**) на адрес `/api/v1/auth/signup/`. На указанный адрес почты придет письмо с кодом подтверждения (**confirmation_code**), который вместе с именем пользователя необходимо отправить на `/api/v1/auth/token/` для получения JWT-токена, дающего доступ на добавление отзывов и комментариев. По истечении срока действия текущего токена, необходимо снова отправить POST-запрос с кодом подтверждения и именем пользователя на указанный адрес. Утерянный код подтверждения можно восстановить повторным запросом на `/api/v1/auth/signup/`.

Пользователей может создавать и администратор через админ-зону сайта или через API. Но созданный пользователь все равно должен сделать запросы для получения кода подтверждения и JWT-токена.

### Как запустить проект
Клонируйте репозиторий и перейдите в него в командной строке:
```
git clone https://github.com/Dron-71/api_yamdb.git
```
```
cd api_yamdb
```
Создайте и активируйте виртуальное окружение:
```
# for Mac, Linux
python3 -m venv env

# Windows
python -m venv env
```
```
source env/bin/activate
```
Установите зависимости из файла requirements.txt:
```
python -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```

Выполните миграции:
```
python manage.py migrate
```
Заполните базу данных данными из файлов в директории `/static/data`:
```
python manage.py upload_csv
```
Запустите проект:
```
python manage.py runserver
```
Для удаления всех записей в базе данных можете использовать management-команду *clean_database*:
```
python manage.py clean_database
```

### Схема базы данных проекта
![Схема базы данных](db_schema.png)

### Как работать с проектом
#### 1. /auth/signup/
- **Описание**: регистрация нового пользователя в системе и/ или получение кода подтверждения.
- **Аутентификация**: без токена.
- **Права доступа**: все пользователи.
- **Типы запросов**: POST.
Пример запроса:
```
POST: /api/v1/auth/signup/
{
	"username": "GhostOfMadness",
	"email": "foo@bar.com"
}
```
Пример ответа:
```
{
	"username": "GhostOfMadness",
	"email": "foo@bar.com"
}
```
#### 2. /auth/token/
- **Описание**: получение JWT-токена.
- **Аутентификация**: без токена.
- **Права доступа**: все пользователи.
- **Типы запросов**: POST.
Пример запроса:
```
POST: /api/v1/auth/token/
{
	"username": "GhostOfMadness",
	"confirmation_code": "4598e8a0494591641bcd8315c33861dded55c6a29ca1fd784c0f84d8494df082"
}
```
Пример ответа:
```
{
	"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjgyOTI5NjYwLCJqdGkiOiI3MjczZDM5YjMwYzE0ZmU0OTljOTQ4NjdjZjU3OTUxNCIsInVzZXJfaWQiOjE4fQ.T82Bn_2svBtdOp7BmMtwLDxNw4BfvUENaw9oGnKe_FI",
}
```
#### 3. /users/
- **Описание**: получение списка всех пользователей проекта/ создание нового пользователя в системе.
- **Аутентификация**: JWT-токен.
- **Права доступа**: Администратор, Суперпользователь.
- **Типы запросов**: GET, POST.
Пример GET-запроса:
```
GET: /api/v1/users/
```
Пример ответа:
```
{
	"count": 2,
	"next": null,
	"previous": null,
	"results": [
		{
			"username": "angry",
			"email": "angry@yamdb.fake",
			"first_name": "",
			"last_name": "",
			"bio": "",
			"role": "moderator"
		},
		{
			"username": "bingobongo",
			"email": "bingobongo@yamdb.fake",
			"first_name": "",
			"last_name": "",
			"bio": "",
			"role": "user"
		}
	]
}
```
Пример POST-запроса:
```
POST: /api/v1/users/
{
	"username": "new_moderator",
	"email": "new_moderator@bar.com",
	"first_name": "John",
	"last_name": "Doe",
	"bio": "Test request to create a new user",
	"role": "moderator"
}
```
Пример ответа:
```
{
	"username": "new_moderator",
	"email": "new_moderator@bar.com",
	"first_name": "John",
	"last_name": "Doe",
	"bio": "Test request to create a new user",
	"role": "moderator"
}
```
#### 4. /users/{username}/
- **Описание**: получение, изменение или удаление информации о конкретном пользователе.
- **Аутентификация**: JWT-токен.
- **Права доступа**: Администратор, Суперпользователь.
- **Типы запросов**: GET, PATCH, DELETE.
Пример GET-запроса:
```
GET: /api/v1/users/new_moderator/
```
Пример ответа:
```
{
	"username": "new_moderator",
	"email": "new_moderator@bar.com",
	"first_name": "John",
	"last_name": "Doe",
	"bio": "Test request to create a new user",
	"role": "moderator"
}
```
Пример PATCH-запроса:
```
PATCH: /api/v1/users/new_moderator/
{
	"first_name": "Jane",
	"last_name": "Doe",
	"bio": "Test request to update information about user"
}
```
Пример ответа:
```
{
	"username": "new_moderator",
	"email": "new_moderator@bar.com",
	"first_name": "Jane",
	"last_name": "Doe",
	"bio": "Test request to update information about user",
	"role": "moderator"
}
```
Пример DELETE-запроса:
```
DELETE: /api/v1/users/new_moderator/
```
#### 5. /users/me/
- **Описание**: получение или изменение информации о себе.
- **Аутентификация**: JWT-токен.
- **Права доступа**: Аутентицифированный пользователь.
- **Типы запросов**: GET, PATCH.
Пример GET-запроса:
```
GET: /api/v1/users/me/
```
Пример ответа:
```
{
	"username": "new_moderator",
	"email": "new_moderator@bar.com",
	"first_name": "Jane",
	"last_name": "Doe",
	"bio": "Test request to update information about user",
	"role": "moderator"
}
```
Пример PATCH-запроса:
```
PATCH: /api/v1/users/me/
{
	"bio": "I can change all fields except for 'role'."
}
```
Пример ответа:
```
{
	"username": "new_moderator",
	"email": "new_moderator@bar.com",
	"first_name": "Jane",
	"last_name": "Doe",
	"bio": "I can change all fields except for 'role'.",
	"role": "moderator"
}
```
#### 6. /categories/
- **Описание**: получение списка имеющихся категорий или добавление новой категории.
- **Аутентификация**: JWT-токен.
- **Права доступа**: Администратор, Суперпользователь.
- **Типы запросов**: GET, POST.
Пример GET-запроса:
```
GET: /api/v1/categories/
```
Пример ответа:
```
{
	"count": 3,
	"next": null,
	"previous": null,
	"results": [
		{
			"name": "Книга",
			"slug": "book"
		},
		{
			"name": "Фильм",
			"slug": "movie"
		},
		{
			"name": "Музыка",
			"slug": "music"
		}
	]
}
```
Пример POST-запроса:
```
POST: /api/v1/categories/
{
	"name": "Сериал",
	"slug": "tv_series"
}
```
Пример ответа:
```
{
	"name": "Сериал",
	"slug": "tv_series"
}
```
#### 7. /categories/{slug}/
- **Описание**: удаление категории.
- **Аутентификация**: JWT-токен.
- **Права доступа**: Администратор, Суперпользователь.
- **Типы запросов**: DELETE.
Пример запроса:
```
DELETE: /api/v1/categories/tv_series/
```
#### 8. /genres/
- **Описание**: получение списка имеющихся жанров или добавление нового жанра.
- **Аутентификация**: JWT-токен.
- **Права доступа**: Администратор, Суперпользователь.
- **Типы запросов**: GET, POST.
Пример GET-запроса:
```
GET: /api/v1/genres/
```
Пример ответа:
```
{
	"count": 15,
	"http://127.0.0.1:8000/api/v1/genres/?page=2",
	"previous": null,
	"results": [
		{
			"name": "Баллада",
			"slug": "ballad"
		},
		{
			"name": "Комедия",
			"slug": "comedy"
		},
		{
			"name": "Детектив",
			"slug": "detective"
		},
		...
	]
}
```
Пример POST-запроса:
```
POST: /api/v1/genres/
{
	"name": "Фэнтези",
	"slug": "fantasy"
}
```
Пример ответа:
```
{
	"name": "Фэнтези",
	"slug": "fantasy"
}
```
#### 9. /genres/{slug}/
- **Описание**: удаление жанра.
- **Аутентификация**: JWT-токен.
- **Права доступа**: Администратор, Суперпользователь.
- **Типы запросов**: DELETE.
Пример запроса:
```
DELETE: /api/v1/genres/drama/
```
#### 10. /titles/
- **Описание**: получение списка имеющихся произведений или добавление нового произведения.
- **Аутентификация**: без токена (чтение данных), JWT-токен (запись данных).
- **Права доступа**: все пользователи (чтение данных); Администратор, Суперпользователь (запись данных).
- **Типы запросов**: GET, POST.
Пример GET-запроса:
```
GET: /api/v1/titles/
```
Пример ответа:
```
{
	"count": 32,
	"next": "http://127.0.0.1:8000/api/v1/titles/?page=2",
	"previous": null,
	"results": [
		{
			"id": 3,
			"name": "12 разгневанных мужчин",
			"year": 1957,
			"rating": 8,
			"description": null,
			"genre": [
				{
					"name": "Драма",
					"slug": "drama"
				}
			],
			"category": {
				"name": "Фильм",
				"slug": "movie"
			}
		},
		...
	]
}
```
Пример POST-запроса:
```
POST: /api/v1/titles/
{
	"name": "Звездные войны: Изгой-один",
	"year": 2016,
	"category": "movie",
	"genre": ["drama", "sci-fi"],
	"description": "Спин-офф легендарной саги!"
}
```
Пример ответа:
```
{
	"id": 33,
	"name": "Звездные войны: Изгой-один",
	"year": 2016,
	"rating": null,
	"description": "Спин-офф легендарной саги!",
	"genre": [
		{
			"name": "Драма",
			"slug": "drama"
		},
		{
			"name": "Фантастика",
			"slug": "sci-fi"
		}
	],
	"category": {
		"name": "Фильм",
		"slug": "movie"
	}
}
```
#### 11. /titles/{titles_id}/
- **Описание**: получение, изменение или удаление информации о произведении.
- **Аутентификация**: без токена (чтение данных), JWT-токен (изменение данных).
- **Права доступа**: все пользователи (чтение данных); Администратор, Суперпользователь (изменение данных).
- **Типы запросов**: GET, PATCH, DELETE.
Пример GET-запроса:
```
GET: /api/v1/titles/33/
```
Пример ответа:
```
{
	"id": 33,
	"name": "Звездные войны: Изгой-один",
	"year": 2016,
	"rating": null,
	"description": "Спин-офф легендарной саги!",
	"genre": [
		{
			"name": "Драма",
			"slug": "drama"
		},
		{
			"name": "Фантастика",
			"slug": "sci-fi"
		}
	],
	"category": {
		"name": "Фильм",
		"slug": "movie"
	}
}
```
Пример PATCH -запроса:
```
PATCH: /api/v1/titles/33/
{
	"name": "Изгой-один. Звездные войны: Истории"
}
```
Пример ответа:
```
{
	"id": 33,
	"name": "Изгой-один. Звездные войны: Истории",
	"year": 2016,
	"rating": null,
	"description": "Спин-офф легендарной саги!",
	"genre": [
		{
			"name": "Драма",
			"slug": "drama"
		},
		{
			"name": "Фантастика",
			"slug": "sci-fi"
		}
	],
	"category": {
		"name": "Фильм",
		"slug": "movie"
	}
}
```
Пример DELETE-запроса:
```
DELETE: /api/v1/titles/33/
```
#### 12. titles/{title_id}/reviews/
- **Описание**: получение списка имеющихся отзывов или добавление нового отзыва к конкретному произведению.
- **Аутентификация**: без токена (чтение данных), JWT-токен (запись данных).
- **Права доступа**: все пользователи (чтение данных); Аутентифицированный пользователь (запись данных).
- **Типы запросов**: GET, POST.
Пример GET-запроса:
```
GET: /api/v1/titles/1/reviews/
```
Пример ответа:
```
{
	"count": 2,
	"next": null,
	"previous": null,
	"results": [
		{
			"id": 1,
			"text": "Ставлю десять звёзд!\n...Эти голоса были чище и светлее тех, о которых мечтали в этом сером, убогом месте. Как будто две птички влетели и своими голосами развеяли стены наших клеток, и на короткий миг каждый человек в Шоушенке почувствовал себя свободным.",
			"author": "bingobongo",
			"score": 10,
			"pub_date": "2023-04-03T09:34:19.102465Z"
		},
		{
			"id": 2,
			"text": "Не привыкай\n«Эти стены имеют одно свойство: сначала ты их ненавидишь, потом привыкаешь, а потом не можешь без них жить»",
			"author": "capt_obvious",
			"score": 10,
			"pub_date": "2023-04-03T09:34:19.102491Z"
		}
	]
}
```
Пример POST-запроса:
```
POST: /api/v1/titles/1/reviews/
{
	"text": "Замечательный фильм!",
	"score": 9
}
```
Пример ответа:
```
{
	"id": 76,
	"text": "Замечательный фильм!",
	"author": "dasha",
	"score": 9,
	"pub_date": "2023-04-03T14:46:38.814565Z"
}
```
#### 13. /titles/{titles_id}/reviews/{review_id}/
- **Описание**: получение, изменение или удаление отзыва.
- **Аутентификация**: без токена (чтение данных), JWT-токен (изменение данных).
- **Права доступа**: все пользователи (чтение данных); Автор отзыва, Модератор, Администратор, Суперпользователь (изменение данных).
- **Типы запросов**: GET, PATCH, DELETE.
Пример GET-запроса:
```
GET: /api/v1/titles/33/reviews/76/
```
Пример ответа:
```
{
	"id": 76,
	"text": "Замечательный фильм!",
	"author": "dasha",
	"score": 9,
	"pub_date": "2023-04-03T14:46:38.814565Z"
}
```
Пример PATCH -запроса:
```
PATCH: /api/v1/titles/33/reviews/76/
{
	"text": "Хороший фильм."
}
```
Пример ответа:
```
{
	"id": 76,
	"text": "Хороший фильм.",
	"author": "dasha",
	"score": 9,
	"pub_date": "2023-04-03T14:46:38.814565Z"
}
```
Пример DELETE-запроса:
```
DELETE: /api/v1/titles/33/reviews/76/
```
#### 14. titles/{title_id}/reviews/{review_id}/comments/
- **Описание**: получение списка имеющихся комментариев  или добавление нового комментария к конкретному отзыву на произведение.
- **Аутентификация**: без токена (чтение данных), JWT-токен (запись данных).
- **Права доступа**: все пользователи (чтение данных); Аутентифицированный пользователь (запись данных).
- **Типы запросов**: GET, POST.
Пример GET-запроса:
```
GET: /api/v1/titles/5/reviews/6/comments/
```
Пример ответа:
```
{
	"count": 3,
	"next": null,
	"previous": null,
	"results": [
		{
			"id": 2,
			"text": "Ну надо же, не нашлось ничего лучшего, кроме как прокомментировать разговор про гамбургеры, будто в фильме ничего важнее этого нет",
			"author": "capt_obvious",
			"pub_date": "2023-04-03T09:34:19.107031Z"
		},
		{
			"id": 1,
			"text": "Ничего подобного, в фильме всё не так, и программирование тут вообще ни при чём!",
			"author": "faust",
			"pub_date": "2023-04-03T09:34:19.107013Z"
		},
		{
			"id": 3,
			"text": "Кстати, а что такое \"четверть фунта\"? В граммах это сколько?",
			"author": "reviewer",
			"pub_date": "2023-04-03T09:34:19.107042Z"
		}
	]
}
```
Пример POST-запроса:
```
POST: /api/v1/titles/5/reviews/6/comments/
{
	"text": "Просто комментарий"
}
```
Пример ответа:
```
{
	"id": 4,
	"text": "Просто комментарий",
	"author": "dasha",
	"pub_date": "2023-04-03T14:58:51.227415Z"
}
```
#### 15. /titles/{titles_id}/reviews/{review_id}/comments/{comment_id}/
- **Описание**: получение, изменение или удаление комментария.
- **Аутентификация**: без токена (чтение данных), JWT-токен (изменение данных).
- **Права доступа**: все пользователи (чтение данных); Автор комментария, Модератор, Администратор, Суперпользователь (изменение данных).
- **Типы запросов**: GET, PATCH, DELETE.
Пример GET-запроса:
```
GET: /api/v1/titles/5/reviews/6/comments/4/
```
Пример ответа:
```
{
	"id": 4,
	"text": "Просто комментарий",
	"author": "dasha",
	"pub_date": "2023-04-03T14:58:51.227415Z"
}
```
Пример PATCH -запроса:
```
PATCH: /api/v1/titles/33/reviews/76/
{
	"text": "Измененный комментарий."
}
```
Пример ответа:
```
{
	"id": 4,
	"text": "Измененный комментарий.",
	"author": "dasha",
	"pub_date": "2023-04-03T14:58:51.227415Z"
}
```
Пример DELETE-запроса:
```
DELETE: /api/v1/titles/5/reviews/6/comments/4/
```
Подробную документацию с описанием допустимых кодов ответа и характеристиками запросов можно посмотреть на `/redoc/`.
