from db_connection import get_db
import time, datetime


def post_tag(tag_name, url):
    conn = get_db()
    c = conn.cursor()
    unix = int(time.time())
    post_time = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
    try:
        c.execute("""INSERT INTO tags VALUES (NULL, ?, ?, ?)""", (
            tag_name, url, post_time))
        conn.commit()
    except Exception:
        conn.rollback()


def get_tag_details(url):
    conn = get_db()
    c = conn.cursor()
    try:
        c.execute("""SELECT * FROM tags where url = ?""", (url,))
        rows = c.fetchall()
        if len(rows) == 0:
            return False
        return rows
    except Exception as e:
        return e


def delete_tag(tag_id):
    conn = get_db()
    c = conn.cursor()
    try:
        c.execute("""DELETE FROM tags WHERE tag_id = ?""", (tag_id,))
        conn.commit()
    except Exception:
        conn.rollback()


def get_tag_by_url(url):
    conn = get_db()
    c = conn.cursor()
    try:
        c.execute("""SELECT * FROM tags where url = ?""", (url,))
        rows = c.fetchall()
        if len(rows) == 0:
            return False
        return rows
    except Exception as e:
        return e


def get_tag_by_tag_name(tag_name):
    conn = get_db()
    c = conn.cursor()
    try:
        c.execute("""SELECT tag_name, url FROM tags where tag_name = ?""", (tag_name,))
        rows = c.fetchall()
        if len(rows) == 0:
            return False
        row_headers = [x[0] for x in c.description]
        tags = []
        for tag in rows:
            tags.append(dict(zip(row_headers, tag)))
        return tags
    except Exception as e:
        return e


def get_tags_by_url(url):
    conn = get_db()
    c = conn.cursor()
    try:
        c.execute("""SELECT tag_name, url FROM tags where url = ?""", (url,))
        rows = c.fetchall()
        if len(rows) == 0:
            return False
        row_headers = [x[0] for x in c.description]
        tags = []
        for tag in rows:
            tags.append(dict(zip(row_headers, tag)))
        return tags
    except Exception as e:
        return e


def get_tags_metadata(n):
    conn = get_db()
    c = conn.cursor()

    c.execute(
        """SELECT tag, title, url  FROM tags ORDER BY post_time LIMIT ?""", (n,))
    row_headers = [x[0] for x in c.description]
    rows = c.fetchall()
    tags = []

    for tag in rows:
        tags.append(dict(zip(row_headers, tag)))
    return tags
