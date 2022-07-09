# API_YAmdb

## Описание

Проект YaMDb собирает отзывы (Review) пользователей на произведения (Titles). Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку. В каждой категории есть произведения: книги, фильмы или музыка. Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Насекомые» и вторая сюита Баха.
Произведению может быть присвоен жанр (Genre) из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). Новые жанры может создавать только администратор.
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы (Review) и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.

В данном проекте были отработаны навыки командной работы в GIT, закреплены знания по созданию REST API, а так же изолированной среды в Docker.
Кроме того в данной работе реализован метод разработки CI/CD. При внесении изменений в проект и отправки их с локального компьютера в репозиторий на GitHub, производяться следующие процессы с помощью Github Actions:

1. Проводиться тестирование на соответствие кода PEP8, а так же запуск pytest из репозитория.
3. Сборка и доставка докер-образа для контейнера web на Docker Hub
4. Автоматический деплой проекта на боевой сервер
5. Отправка уведомления в Telegram о том, что процесс деплоя успешно завершился. 


## Как запустить проект

Для успешного использования проекта понадобится добавить Секреты (переменные среды в Github) в свой репозиторий после fork-а:
- DOCKER_USERNAME (имя пользователя в Docker Hub)
- DOCKER_PASSWORD (пароль от учётной записи в Docker Hub)
- HOST (ip-дрес боевого сервера)
- USER (имя пользоватля для подключения к серверу)
- PASSPHRASE (фраза-пароль для использования SSH-ключа)
- SSH-KEY (закрытый ключ компьютера с доступом к серверу)
- TELEGRAM_TO (id Вашего аккаунта в Telegram)
- TELEGRAM_TOKEN (токен бота для рассылки уведомления)
- MAIL (почта с которой будет рассылаться токен для подтверждения авторизации)
- MAIL_PASSWORD (пароль от почты выше)
- SECRET_KEY (ключ Django-проекта)
- DB_ENGINE (используемая база, по умолчанию django.db.backends.postgresql)
- DB_NAME (имя базы)
- POSTGRES_USER (пользователь базы)
- POSTGRES_PASSWORD (пароль пользователя)
- DB_HOST (хост)
- DB_PORT (порт)


После этого выполнить следующие действия:

1. Клонировать репозиторий:

```sh
git clone git@github.com:AlexeyAnanchenko/api_yamdb-docker.git
```
2. Создать папку .github/workflows/ и переместить туда файл yamdb_workflow.yml из проекта

3. Зайти на свой удаленный сервер и остановить службу nginx (если запущена):

```sh
sudo systemctl stop nginx
```

4. Установите docker и docker-compose (если не установлено), с этим вам поможет официальная документация: https://docs.docker.com/compose/install

5. Скопируйте файлы docker-compose.yaml и nginx/default.conf из вашего проекта на сервер в home/<ваш_username>/docker-compose.yaml и home/<ваш_username>/nginx/default.conf соответственно.


__Далее после каждого пуша проект будет автоматически разворачиваться на боевом сервере__

__Для корректной работы, после первого деплоя надо сделать следующие операции в контейнере проекта на сервере__

6. Выполните миграции и создайте суперпользователя:

```sh
sudo docker-compose exec web python manage.py migrate
```

```sh
sudo docker-compose exec web python manage.py createsuperuser
```

7. Соберите статику:

```sh
sudo docker-compose exec web python manage.py collectstatic --no-input
```

8. Загрузите тестовые данные с помощю специально подготовленной менеджмент-команды:

```sh
sudo docker-compose exec web python manage.py import-csv
```

## Основные адреса проекта:

ip - это IP вашего боевого сервера, где будет деплой проекта

- http://ip/api/v1/ (основная страница проекта)
- http://ip/admin (админка)
- http://ip/redoc (подробное описание всех адресов и доступов проекта)


## Как зарегистрироваться через API:

1. Регистрация нового пользователя:

Request (POST-запрос):
```sh
http://ip/api/v1/auth/signup/
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
http://ip/api/v1/auth/token/
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
http://ip/api/v1/titles/
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
http://ip/api/v1/titles/{title_id}/reviews/
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
http://ip/api/v1/users/me/
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