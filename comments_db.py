import datetime
import time

from db_connection import get_db_comments


def post_comment(username, article_name, comment):
    conn = get_db_comments()
    c = conn.cursor()
    unix = int(time.time())
    post_time = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
    try:
        c.execute("""INSERT into comments VALUES (NULL,?,?,?,?)""", (username, article_name, comment, post_time))
        conn.commit()

    except Exception:
        conn.rollback()


def count_comments(article_name):
    conn = get_db_comments()
    c = conn.cursor()
    c.execute("""SELECT COUNT(*) from comments WHERE article_name = (?)""", (article_name,))
    rows = c.fetchone()
    n_comments = rows[0]
    return n_comments


def get_comments(article_name, no_of_comments):
    conn = get_db_comments()
    c = conn.cursor()
    c.execute("""SELECT * from comments where article_name = (?) ORDER BY post_time DESC LIMIT (?)""", (
        article_name, no_of_comments))
    rows = c.fetchall()
    if rows:
        row_headers = [x[0] for x in c.description]
        comments = []
        for comment in rows:
            comments.append(dict(zip(row_headers, comment)))
        return comments
    else:
        return False

def get_comment(comment_id):
    conn = get_db_comments()
    c = conn.cursor()
    c.execute("""SELECT * FROM comments WHERE comment_id = (?)""", (comment_id,))
    row = c.fetchone()
    if row:
        return True
    else:
        return False

def delete_comment(comment_id):
    conn = get_db_comments()
    c = conn.cursor()
    c.execute("""DELETE FROM comments WHERE comment_id = (?)""", (comment_id,))
    conn.commit()