import datetime
import time

from db_connection import get_db_articles


def post_article(username, text, author, title, url):
    conn = get_db_articles()
    c = conn.cursor()
    unix = int(time.time())
    post_time = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
    last_updated_time = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
    try:
        c.execute("""INSERT INTO articles VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)""", (
            username, text, author, title, url, post_time, last_updated_time))
        conn.commit()
    except Exception:
        conn.rollback()


def get_article_details(username, title):
    conn = get_db_articles()
    c = conn.cursor()
    try:
        c.execute("""SELECT * FROM articles where username = ? AND title = ?""", (username, title))
        rows = c.fetchall()
        if len(rows) == 0:
            return False
        return rows
    except Exception as e:
        return e


def get_article_by_url(url):
    conn = get_db_articles()
    c = conn.cursor()
    try:
        c.execute("""SELECT * FROM articles where url = ?""", (url,))
        rows = c.fetchall()
        if len(rows) == 0:
            return False
        return rows
    except Exception as e:
        return e


def edit_article(author, text, article_id):
    conn = get_db_articles()
    c = conn.cursor()
    unix = int(time.time())
    last_updated_time = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
    try:
        c.execute("""UPDATE articles SET text = ?, author = ?,last_updated_time = ? WHERE article_id = ?""",
                  (text, author, last_updated_time, article_id))
        conn.commit()
    except Exception:
        conn.rollback()


def delete_article(article_id):
    conn = get_db_articles()
    c = conn.cursor()
    try:
        c.execute("""DELETE FROM articles WHERE article_id = ?""", (article_id,))
        conn.commit()
    except Exception:
        conn.rollback()


def get_article(title):
    conn = get_db_articles()
    c = conn.cursor()
    try:
        c.execute("""SELECT * FROM articles WHERE title = ? ORDER BY post_time desc""", (title,))
        rows = c.fetchall()
        if len(rows) == 0:
            return False
        return rows
    except Exception as e:
        return e


def get_n_articles(n):
    conn = get_db_articles()
    c = conn.cursor()
    c.execute(
        """SELECT text, author, title, post_time, last_updated_time FROM articles ORDER BY \
        post_time desc LIMIT ?""", (n,))
    rows = c.fetchall()
    if len(rows) == 0:
        return False
    row_headers = [x[0] for x in c.description]
    articles = []
    for article in rows:
        articles.append(dict(zip(row_headers, article)))
    return articles


def get_articles_metadata(n):
    conn = get_db_articles()
    c = conn.cursor()
    c.execute("""SELECT text, author, title FROM articles ORDER BY post_time desc LIMIT ?""", (n,))
    rows = c.fetchall()
    if len(rows) == 0:
        return False
    row_headers = [x[0] for x in c.description]
    articles = []
    for article in rows:
        articles.append(dict(zip(row_headers, article)))
    return articles
