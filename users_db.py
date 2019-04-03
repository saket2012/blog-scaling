from db_connection import get_db
import hashlib
from passlib.hash import sha256_crypt

def create_user(username, password, display_name):
    hash_password = encode_password(password)
    conn = get_db()
    c = conn.cursor()
    try:
        c.execute("""INSERT into users values (NULL, ?, ?, ?)""", (
            username, hash_password, display_name))
        conn.commit()
    except Exception:
        conn.rollback()


def update_password(username, new_password):
    hash_password = encode_password(new_password)
    conn = get_db()
    c = conn.cursor()
    try:
        c.execute("""UPDATE users SET password = ? WHERE username = ?""", (
            hash_password, username))
        conn.commit()
    except Exception:
        conn.rollback()


def delete_user(username):
    conn = get_db()
    c = conn.cursor()
    try:
        c.execute("""DELETE FROM users WHERE username = ?""", (username,))
        conn.commit()
    except Exception:
        conn.rollback()


def get_user_details(username):
    conn = get_db()
    c = conn.cursor()
    c.execute("""SELECT * FROM users WHERE username = ?""", (username,))
    rows = c.fetchall()
    if len(rows) == 0:
        return False
    return rows


def encode_password(password):
    hash_password = sha256_crypt.encrypt(password)
    return hash_password
