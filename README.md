# api_yamdb

## Описание
Данный проект написан с целью отработать навык работы с Docker. Внутри контейнера расположен ранее созданный проект api_yamdb (его описание расположено ниже).

Проект YaMDb собирает отзывы (Review) пользователей на произведения (Titles). Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку. В каждой категории есть произведения: книги, фильмы или музыка. Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Насекомые» и вторая сюита Баха.
Произведению может быть присвоен жанр (Genre) из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). Новые жанры может создавать только администратор.
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы (Review) и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.

## Как запустить проект
Клонировать репозиторий:

```sh
git clone git@github.com:AlexeyAnanchenko/infra_sp2.git
```

Создайте файл .env в директории nginx/ и заполните перменные окружения:
- MAIL=_почта с которой будет рассылаться токен_,
- PASSWORD=_пароль от почты выше_,
- SECRET_KEY=_ключ Джанго проекта_,
- DB_ENGINE=_django.db.backends.postgresql_,
- DB_NAME=_имя базы_,
- POSTGRES_USER=_пользователь базы_,
- POSTGRES_PASSWORD=_пароль пользователя_,
- DB_HOST=_хост_,
- DB_PORT=_порт_,


Запустить docker-compose:

```sh
sudo docker-compose up -d
```

Выполните миграции и создайте суперпользователя:

```sh
sudo docker-compose exec web python manage.py migrate
```

```sh
sudo docker-compose exec web python manage.py createsuperuser
```

Соберите статику:

```sh
sudo docker-compose exec web python manage.py collectstatic --no-input
```

Загрузите тестовые данные:

```sh
sudo docker-compose exec web python manage.py import-csv
```

Теперь проект доступен по адресу http://localhost/.

## Как зарегистрироваться через API:

1. Регистрация нового пользователя:

Request (POST-запрос):
```sh
http://127.0.0.1:8000/api/v1/auth/signup/
```

```sh
{

    "email": "string",
    "username": "string"

}
```

Response:
```sh
{

    "email": "string",
    "username": "string"

}
```

2. Получение Токена:

Request (POST-запрос):
```sh
http://127.0.0.1:8000/api/v1/auth/token/
```

```sh
{

    "username": "string",
    "confirmation_code": "string"

}
```

Response:
```sh
{

    "token": "string"

}
```

## Примеры запросов к API

1. Просмотреть список всех произведений:

Request (GET-запрос):
```sh
http://127.0.0.1:8000/api/v1/titles/
```

Response:
```sh
[

{

    "count": 0,
    "next": "string",
    "previous": "string",
    "results": 

[

{

    "id": 0,
    "name": "string",
    "year": 0,
    "rating": 0,
    "description": "string",
    "genre": 

[

    {}

],
"category": 

                {
                    "name": "string",
                    "slug": "string"
                }
            }
        ]
    }

]
```


2. Добавить отзыв к произведению

Request (POST-запрос):
```sh
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
```

```sh
{

    "text": "string",
    "score": 1

}
```

Response:
```sh
{

    "id": 0,
    "text": "string",
    "author": "string",
    "score": 1,
    "pub_date": "2019-08-24T14:15:22Z"

}
```

3. Изменить данные своей учётной записи:

Request (PATCH-запрос):
```sh
http://127.0.0.1:8000/api/v1/users/me/
```

```sh
{

    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "bio": "string"

}
```

Response:
```sh
{

    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "bio": "string",
    "role": "user"

}
```

## Автор проекта

- Ананченко Алексей

## Лицензия

MIT License

Copyright (c) 2022 AlexeyAn

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

https://github.com/AlexeyAnanchenko/api_yamdb-docker/blob/main/LICENSE