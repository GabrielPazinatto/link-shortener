import sqlite3

from fastapi import HTTPException
from queries import Queries

_DB_TABLE_CREATION_FILE_PATH: str = "../sql/tables.sql"
_DB_FILE_PATH: str = "../sql/database.db"

class DataBase:
    def __init__(self):
        self._db_connection: sqlite3.Connection = sqlite3.connect(_DB_FILE_PATH)
        self._db_cursor: sqlite3.Cursor = self._db_connection.cursor()
        self._queries: Queries = Queries()

        with open(_DB_TABLE_CREATION_FILE_PATH) as tables:
            DB_CREATE_TABLES_SCRIPT = tables.read()

        self._db_cursor.executescript(DB_CREATE_TABLES_SCRIPT)
        self._db_connection.commit()

    def execute_query(self, query: str):
        response = self._db_cursor.execute(query).fetchall()
        self._db_connection.commit()
        return response

    def login(self, username: str, password: str):
        response = self._queries.login(
            username=username, password=password, cursor=self._db_cursor)
        self._db_connection.commit()
        return response
        
    def get_urls_from_user(self, user_id: int):
        return self._queries.get_urls_from_user(user_id=user_id, cursor=self._db_cursor)

    def get_long_url(self, shortened_url: str):
        return self._queries.get_long_url(
            shortened_url=shortened_url, cursor=self._db_cursor
        )

    def add_url(self, user_id: str, url: str, short_url: str):
        self._queries.add_url(
            user_id=user_id, url=url, short_url=short_url, cursor=self._db_cursor
        )
        self._db_connection.commit()

    def add_user(self, username: str, password: str):
        try:
            self._queries.add_user(
                username=username, password=password, cursor=self._db_cursor
            )
            self._db_connection.commit()

        except sqlite3.IntegrityError as e:
            raise HTTPException(status_code=409, detail=str(e))

    def delete_user(self, user_id: int):
        self._queries.delete_user(user_id=user_id, cursor=self._db_cursor)
        self._db_connection.commit()

    def delete_url(self, url_id: int):
        self._queries.delete_url(url_id=url_id, cursor=self._db_cursor)
        self._db_connection.commit()
