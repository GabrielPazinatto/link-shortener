import sqlite3
import json
from typing import Iterable

from fastapi import HTTPException

def jsonify_data(data:Iterable, cursor: sqlite3.Cursor) -> str:
    cols = [desc[0] for desc in cursor.description]
    data = [dict(zip(cols, row)) for row in data]
    return json.dumps(data[0])

class Queries:
    def __init__(self):
        pass

    ######################
    #   GET FROM DB      #
    ######################

    # Select all urls belonging to an user
    def get_urls_from_user(self, user_id: int, cursor: sqlite3.Cursor) -> list:
        return cursor.execute(
            "SELECT url, short_url FROM urls WHERE owner_id = ?;", (user_id,)
        ).fetchall()

    # Select the full url from the short url
    def get_long_url(self, shortened_url: str, cursor: sqlite3.Cursor, ) -> str:
        return cursor.execute(
            "SELECT url FROM urls WHERE short_url = ?;", (shortened_url,)
        ).fetchone()[0]
    
    def check_user_exists(self, username:str, cursor: sqlite3.Cursor) -> bool:
        return cursor.execute(
            "SELECT * FROM users WHERE username = ?;", (username,)
        ).fetchone()

    def login(self, username: str, password: str, cursor: sqlite3.Cursor):
        if not self.check_user_exists(username, cursor):
            raise HTTPException(status_code=404, detail="User not found")
    
        data = cursor.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?;", (username, password)
        ).fetchone()

        if data is None:
            raise HTTPException(status_code=404, detail="Wrong Password")

        return jsonify_data([data], cursor)

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
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?);",
                (username, password),
            )

        # except sqlite3.IntegrityError as e:
        #     if "NOT NULL constraint failed: users.username" in str(e):
        #         return "Username cannot be empty"
            
        #     elif "NOT NULL constraint failed: users.password" in str(e):
        #         return "Password cannot be empty"

        #     elif "UNIQUE constraint failed: users.username" in str(e):
        #         return "Username already exists"

    ######################
    #   DELETE FROM DB   #
    ######################

    # Delete an user
    def delete_user(self, user_id: int, cursor: sqlite3.Cursor) -> None:
        cursor.execute("DELETE FROM users WHERE id = ?;", (user_id,))

    # Delete a shortened url
    def delete_url(self, url_id: int, cursor: sqlite3.Cursor) -> None:
        cursor.execute("DELETE FROM urls WHERE id = ?;", (url_id,))
