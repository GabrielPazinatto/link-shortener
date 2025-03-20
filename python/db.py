import os
from dotenv import find_dotenv, load_dotenv
from psycopg2 import pool

from python.queries import Queries
from python.utils import generate_random_url

_MIN_POOL_CONN = 1
_MAX_POOL_CONN = 10

class DataBase:
    def __init__(self):

        dotenv_path = find_dotenv()
        load_dotenv(dotenv_path)
        connection_string = os.getenv('DATABASE_URL')

        self._connection_pool = pool.SimpleConnectionPool(
            _MIN_POOL_CONN,
            _MAX_POOL_CONN,
            connection_string
        )
        self._db_connection = self._connection_pool.getconn()
        self._db_cursor = self._db_connection.cursor()
        self._queries: Queries = Queries()


    def execute_query(self, query: str) -> any:
        response = self._db_cursor.execute(query).fetchall()
        self._db_connection.commit()
        return response

    def login(self, username: str, password: str) -> dict:
        response = self._queries.login(
            username=username, password=password, cursor=self._db_cursor
        )
        self._db_connection.commit()
        return response

    def get_urls_from_user(self, user_id: int) -> list:
        response = self._queries.get_urls_from_user(
            user_id=user_id, cursor=self._db_cursor
        )
        self._db_connection.commit()
        return response

    def add_user(self, username: str, password: str) -> None:
        self._queries.add_user(
            username=username, password=password, cursor=self._db_cursor
        )
        self._db_connection.commit()

    def get_long_url(self, shortened_url: str) -> str:
        return self._queries.get_long_url(
            shortened_url=shortened_url, cursor=self._db_cursor
        )

    def add_url(self, user_id: str, url: str):
        shortened_url = generate_random_url()

        while self._queries.short_url_exists(shortened_url, self._db_cursor):
            shortened_url = generate_random_url()

        self._queries.add_url(
            user_id=user_id, url=url, short_url=shortened_url, cursor=self._db_cursor
        )
        self._db_connection.commit()

    def delete_user(self, user_id: int):
        self._queries.delete_user(user_id=user_id, cursor=self._db_cursor)
        self._db_connection.commit()

    def delete_url(self, user_id: int, short_urls:list[str]|str):
        if isinstance(short_urls, list):
            for url in short_urls:
                self._queries.delete_url(user_id=user_id, short_url=url, cursor=self._db_cursor)
        else:
            self._queries.delete_url(user_id=user_id, url=short_urls, cursor=self._db_cursor)
            
        self._db_connection.commit()

    