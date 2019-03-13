from db_connection import get_db
import time


def post_article(user_id, text, author, title, url):
    conn = get_db()
    c = conn.cursor()
    post_time = time.time()
    last_updated_time = time.time()
    try:
        c.execute("""INSERT INTO articles VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)""", (
            user_id, text, author, title, url, post_time, last_updated_time))
        conn.commit()
    except Exception:
        conn.rollback()


def get_article_details(user_id, title):
    conn = get_db()
    c = conn.cursor()
    try:
        c.execute("""SELECT * FROM articles where user_id = ? AND title = ?""", (user_id, title))
        rows = c.fetchall()
        if len(rows) == 0:
            return False
        return rows
    except Exception as e:
        return e


def edit_article(title, author, text, article_id):
    conn = get_db()
    c = conn.cursor()
    last_updated_time = time.time()
    try:
        c.execute("""UPDATE articles SET text = ?, author = ?, title = ?,last_updated_time = ? WHERE article_id = ?""",
                  (text, author, title, last_updated_time, article_id))
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


def get_n_articles(n):
    conn = get_db()
    c = conn.cursor()
    c.execute(
        """SELECT text, author, title, url, post_time, post_time FROM articles ORDER BY \
        post_time LIMIT ?""", (n,))
    rows = c.fetchall()
    if len(rows) == 0:
        return False
    row_headers = [x[0] for x in c.description]
    articles = []
    for article in rows:
        articles.append(dict(zip(row_headers, article)))
    return articles


def get_articles_metadata(n):
    conn = get_db()
    c = conn.cursor()
    c.execute(
        """SELECT text, author, title, url  FROM articles ORDER BY post_time LIMIT ?""", (n,))
    row_headers = [x[0] for x in c.description]
    rows = c.fetchall()
    articles = []
    for article in rows:
        articles.append(dict(zip(row_headers, article)))
    return articles
