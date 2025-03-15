from random import choice
import string

def generate_random_url() -> str:
    characters:str = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return ''.join(choice(characters) for i in range(6))