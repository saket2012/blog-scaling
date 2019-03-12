import time, user, articles
from db_connection import get_db
from flask import request



def add_comment(content):
    "Post a new comment on an article"

    auth = request.authorization
    user_details = user.get_user_details(auth.username)

    # Take values from existing Session
    #Re-Check
    user_id = user_details[0]
    article_id = content['article_id']
    display_name = user_details[3]

    #comment_id is auto-increament
    comment = content['comment']
    post_time = time.time()


    conn = get_db()
    c = conn.cursor()
    try:
        c.execute("""INSERT into comments values (?, ?, ?, ?,?)""", (
             user_id, article_id, display_name, comment, post_time))
        conn.commit()

    except Exception:
        conn.rollback()


def delete_comment(content):
    "Delete an individual comment"
    comment_id = content['comment_id']

    conn = get_db()
    c = conn.cursor()
    try:
        c.execute("""DELETE from comments where comment_id  == (?)""", (
            comment_id))
        conn.commit()
    except Exception:
        conn.rollback()


def get_comments_article(content):
    "Retrieve the number of comments on a given article"
    article_id = content['article_id']

    conn = get_db()
    c = conn.cursor()
    try:
        c.execute("""SELECT count(*) from comments where article_id  == (?)""", (
            article_id))
        conn.commit()
    except Exception:
        conn.rollback()


def get_n_comments(content):
    "Retrieve the n most recent comments on a URL"
    article_id = content['article_id']
    n = content['n']

    conn = get_db()
    c = conn.cursor()
    try:
        c.execute("""SELECT * from comments where article_id  == (?) ORDER BY post_time DESC LIMIT (?)""", (
            article_id , n))
        conn.commit()
    except Exception:
        conn.rollback()

