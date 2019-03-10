from db_connection import get_db
import time
from flask import request


def post_article(content):
    text = content['text']
    title = content['title']
    author = content['author']
    timestamp = time.time()
    last_updated_time = time.time()
    conn = get_db()
    c = conn.cursor()
    try:
        c.execute("""INSERT into articles values (?, ?, ?, ?, ?)""", (
            text, title, author, timestamp, last_updated_time))
        conn.commit()
    except Exception:
        conn.rollback()
