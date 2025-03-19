import sqlite3

from fastapi import HTTPException
from utils import jsonify_data


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
        cursor: sqlite3.Cursor,
    ) -> str:
        return cursor.execute(
            "SELECT url FROM urls WHERE short_url = ?;", (shortened_url,)
        ).fetchone()[0]

    def check_user_exists(self, username: str, cursor: sqlite3.Cursor) -> bool:
        return cursor.execute(
            "SELECT * FROM users WHERE username = ?;", (username,)
        ).fetchone()

    def get_user_password(self, username: str, cursor: sqlite3.Cursor) -> str:
        return cursor.execute(
            "SELECT password FROM users WHERE username = ?;", (username,)
        ).fetchone()

    # Select all urls belonging to an user
    def get_urls_from_user(self, user_id: int, cursor: sqlite3.Cursor) -> list:
        response = cursor.execute(
            "SELECT url, short_url FROM urls WHERE owner_id = ?;", (user_id,)
        ).fetchall()
        return jsonify_data(response, cursor)

    def login(self, username: str, password: str, cursor: sqlite3.Cursor):
        if not self.check_user_exists(username, cursor):
            raise HTTPException(status_code=404, detail="User not found")

        data = cursor.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?;",
            (username, password),
        ).fetchone()

        if data is None:
            raise HTTPException(status_code=404, detail="Wrong Password")

        return jsonify_data([data], cursor)

    def short_url_exists(self, short_url: str, cursor: sqlite3.Cursor) -> bool:
        response = cursor.execute(
            "SELECT * FROM urls WHERE short_url = ?;", (short_url,)
        )

        return response.fetchone() is not None

    ######################
    #   ADD TO DB        #
    ######################

    # Create a new shortened url
    def add_url(
        self, user_id: str, url: str, short_url: str, cursor: sqlite3.Cursor
    ) -> None:
        cursor.execute(
            "INSERT INTO urls (owner_id, url, short_url) VALUES (?, ?, ?);",
            (user_id, url, short_url),
        )

    # Create a new user
    def add_user(self, username: str, password: str, cursor: sqlite3.Cursor):
        try:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?);",
                (username, password),
            )
        except sqlite3.IntegrityError:
            raise HTTPException(status_code=409, detail="User already exists")

    ######################
    #   DELETE FROM DB   #
    ######################

    # Delete an user
    def delete_user(self, user_id: int, cursor: sqlite3.Cursor) -> None:
        cursor.execute("DELETE FROM users WHERE id = ?;", (user_id,))

    # Delete a shortened url
    def delete_url(self, user_id: int, short_url: str, cursor: sqlite3.Cursor) -> None:
        cursor.execute(
            """ DELETE FROM urls 
                WHERE owner_id = (SELECT id FROM users WHERE id = ?) 
                AND short_url = ?; """,
            (user_id, short_url),
        )
