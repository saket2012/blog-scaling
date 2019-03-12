from db_connection import get_db
import time


def post_article(user_id, data):
    conn = get_db()
    c = conn.cursor()
    article = data['article']
    author = data['author']
    title = data['title']
    url = data['url']
    post_time = time.time()
    last_updated_time = time.time()
    try:
        c.execute("""INSERT INTO articles VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)""", (
            user_id, article, author, title, url, post_time, last_updated_time))
        conn.commit()
    except Exception:
        conn.rollback()


def get_article_details(user_id, data):
    conn = get_db()
    c = conn.cursor()
    title = data['title']
    try:
        c.execute("""SELECT * FROM articles where user_id = ? AND title = ?""", (user_id, title))
        rows = c.fetchall()
        if len(rows) == 0:
            return False
        return rows
    except Exception as e:
        return e


def edit_article(data, article_id):
    conn = get_db()
    c = conn.cursor()
    article = data['article']
    author = data['author']
    last_updated_time = time.time()
    print(last_updated_time)
    try:
        c.execute("""UPDATE articles SET article = ?, author = ?, last_updated_time = ? WHERE article_id = ?""", (
            article, author, last_updated_time, article_id))
        conn.commit()
    except Exception:
        conn.rollback()


def delete_article(article_id):
    conn = get_db()
    c = conn.cursor()
    try:
        c.execute("""DELETE FROM articles WHERE article_id = ?""", (article_id,))
        conn.commit()
    except Exception:
        conn.rollback()


def get_article(title):
    conn = get_db()
    c = conn.cursor()
    try:
        c.execute("""SELECT * FROM articles where title = ?""", (title,))
        rows = c.fetchall()
        if len(rows) == 0:
            return False
        return rows
    except Exception as e:
        return e
