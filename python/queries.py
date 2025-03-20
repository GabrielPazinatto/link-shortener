import psycopg2
from fastapi import HTTPException
from python.utils import jsonify_data


class Queries:
    def __init__(self):
        pass

    ######################
    #   GET FROM DB      #
    ######################

    # Select the full url from the short url
    def get_long_url(
        self,
        shortened_url: str,
        cursor: psycopg2.extensions.cursor,
    ) -> str:
        query = "SELECT url FROM urls WHERE short_url = %s;"
        cursor.execute(query, (shortened_url,))
        result = cursor.fetchone()
        if result:
            return result[0]
        raise HTTPException(status_code=404, detail="Short URL not found")

    def check_user_exists(
        self, username: str, cursor: psycopg2.extensions.cursor
    ) -> bool:
        query = "SELECT 1 FROM users WHERE username = %s;"
        cursor.execute(query, (username,))
        return cursor.fetchone() is not None

    def get_user_password(
        self, username: str, cursor: psycopg2.extensions.cursor
    ) -> str:
        query = "SELECT password FROM users WHERE username = %s;"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        if result:
            return result[0]
        raise HTTPException(status_code=404, detail="User not found")

    def get_urls_from_user(
        self, user_id: int, cursor: psycopg2.extensions.cursor
    ) -> list:
        query = "SELECT url, short_url FROM urls WHERE owner_id = %s;"
        cursor.execute(query, (user_id,))
        response = cursor.fetchall()
        return jsonify_data(response, cursor)

    def login(self, username: str, password: str, cursor: psycopg2.extensions.cursor):
        if not self.check_user_exists(username, cursor):
            raise HTTPException(status_code=404, detail="User not found")

        query = "SELECT * FROM users WHERE username = %s AND password = %s;"
        cursor.execute(query, (username, password))
        data = cursor.fetchone()

        if data is None:
            raise HTTPException(status_code=404, detail="Wrong Password")

        return jsonify_data([data], cursor)

    def short_url_exists(
        self, short_url: str, cursor: psycopg2.extensions.cursor
    ) -> bool:
        query = "SELECT 1 FROM urls WHERE short_url = %s;"
        cursor.execute(query, (short_url,))
        return cursor.fetchone() is not None

    ######################
    #   ADD TO DB        #
    ######################

    def add_url(
        self,
        user_id: str,
        url: str,
        short_url: str,
        cursor: psycopg2.extensions.cursor,
    ) -> None:
        query = "INSERT INTO urls (owner_id, url, short_url) VALUES (%s, %s, %s);"
        cursor.execute(query, (user_id, url, short_url))

    def add_user(
        self, username: str, password: str, cursor: psycopg2.extensions.cursor
    ):
        query = "INSERT INTO users (username, password) VALUES (%s, %s);"
        try:
            cursor.execute(query, (username, password))
        except psycopg2.IntegrityError:
            raise HTTPException(status_code=409, detail="User already exists")

    ######################
    #   DELETE FROM DB   #
    ######################

    def delete_user(self, user_id: int, cursor: psycopg2.extensions.cursor) -> None:
        query = "DELETE FROM users WHERE id = %s;"
        cursor.execute(query, (user_id,))

    def delete_url(
        self,
        user_id: int,
        short_url: str,
        cursor: psycopg2.extensions.cursor,
    ) -> None:
        query = """
            DELETE FROM urls 
            WHERE owner_id = %s AND short_url = %s;
        """
        cursor.execute(query, (user_id, short_url))
