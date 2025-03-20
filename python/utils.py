from random import choice
import string
from psycopg2.extensions import cursor as PgCursor
from typing import Iterable
import json

def generate_random_url() -> str:
    characters:str = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return ''.join(choice(characters) for i in range(6))


def jsonify_data(data: Iterable, cursor: PgCursor) -> str:
    cols = [desc[0] for desc in cursor.description]
    data = [dict(zip(cols, row)) for row in data]
    return json.dumps(data[0]) if len(data) == 1 else json.dumps(data)