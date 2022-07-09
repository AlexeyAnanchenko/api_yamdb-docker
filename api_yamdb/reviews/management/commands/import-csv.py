from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Команда для загрузки тестовых данных'

    def handle(self, *args, **options):
        import csv
        import os

        import psycopg2
        from dotenv import load_dotenv

        load_dotenv()

        con = psycopg2.connect(
            database=os.getenv('DB_NAME'),
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )
        print('Соединение с базой установлено.')
        cur = con.cursor()

        with open("/app/static/data/category.csv") as f:
            dr = csv.DictReader(f)
            to_db = [(i['id'], i['name'], i['slug']) for i in dr]
        cur.executemany("INSERT INTO reviews_categories (id, name, slug) "
                        "VALUES (%s, %s, %s);", to_db)

        with open("/app/static/data/users.csv") as f:
            dr = csv.DictReader(f)
            to_db = [(
                i['id'], None, False, False,
                True, '2000-01-01 00:00:00-00', i['username'], i['email'],
                i['password'], i['first_name'], i['last_name'], i['bio'],
                i['role']) for i in dr]
        cur.executemany("INSERT INTO reviews_user (id, last_login, "
                        "is_superuser, is_staff, is_active, date_joined, "
                        "username, email, password, first_name, last_name, "
                        "bio, role) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, "
                        "%s, %s, %s, %s, %s);", to_db)

        with open("/app/static/data/genre.csv") as f:
            dr = csv.DictReader(f)
            to_db = [(i['pk'], i['name'], i['slug']) for i in dr]
        cur.executemany("INSERT INTO reviews_genre (id, name, slug) "
                        "VALUES (%s, %s, %s);", to_db)

        with open("/app/static/data/titles.csv") as f:
            dr = csv.DictReader(f)
            to_db = [(
                i['id'], i['name'], i['year'], '', i['category']
            ) for i in dr]
        cur.executemany("INSERT INTO reviews_title (id, name, year, "
                        "description, category_id) VALUES (%s, %s, %s, "
                        "%s, %s);", to_db)

        with open("/app/static/data/genre_title.csv") as f:
            dr = csv.DictReader(f)
            to_db = [(i['id'], i['genre_id'], i['title_id']) for i in dr]
        cur.executemany("INSERT INTO reviews_genretitle (id, genre_id, "
                        "title_id) VALUES (%s, %s, %s);", to_db)

        with open("/app/static/data/review.csv") as f:
            dr = csv.DictReader(f)
            to_db = [(
                i['id'], i['text'], i['score'],
                i['pub_date'], i['author'], i['title_id']
            ) for i in dr]
        cur.executemany("INSERT INTO reviews_review (id, text, score, "
                        "pub_date, author_id, title_id) VALUES (%s, %s, %s, "
                        "%s, %s, %s);", to_db)

        with open("/app/static/data/comments.csv") as f:
            dr = csv.DictReader(f)
            to_db = [(
                i['id'], i['text'], i['pub_date'],
                i['author'], i['review_id']
            ) for i in dr]
        cur.executemany(
            "INSERT INTO reviews_comment (id, text, pub_date, "
            "author_id, review_id) VALUES (%s, %s, %s, %s, %s);",
            to_db
        )

        con.commit()
        con.close()

        print('Загрузка тестовых данных в базу завершена!')
