from db_connection import get_db
import hashlib


def create_user(content):
    username = content['username']
    password = content['password']
    hash_password = encode_password(password)
    display_name = content['display_name']
    conn = get_db()
    c = conn.cursor()
    try:
        c.execute("""INSERT into users values (NULL, ?, ?, ?)""", (
            username, hash_password, display_name))
        conn.commit()
    except Exception:
        conn.rollback()


def update_password(content):
    username = content['username']
    password = content['new_password']
    hash_password = encode_password(password)
    conn = get_db()
    c = conn.cursor()
    try:
        c.execute("""UPDATE users SET password = ? WHERE username = ?""", (
            hash_password, username))
        conn.commit()
    except Exception:
        conn.rollback()


def delete_user(data):
    username = data['username']
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
    hash_password = hashlib.md5(password.encode())
    hash_password = hash_password.hexdigest()
    return hash_password
