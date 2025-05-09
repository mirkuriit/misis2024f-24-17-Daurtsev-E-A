import hashlib


def hash_password(password: str,
                  username: str) -> str:
    salt = username
    return hashlib.md5((password+salt).encode()).hexdigest()

def check_hash_password(password: str,
               username: str,
               hashed_password: str
               ) -> bool:
    return hash_password(password, username) == hashed_password

