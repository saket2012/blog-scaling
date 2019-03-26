import sqlite3

database = 'twitter.db'


def get_db():
    db = sqlite3.connect(database)
    return db


def create_tables():
    conn = get_db()
    c = conn.cursor()
    query = """CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username varchar UNIQUE,
            password varchar,
            display_name varchar)"""
    c.execute(query)
    query = """CREATE TABLE IF NOT EXISTS articles(
            article_id integer PRIMARY KEY AUTOINCREMENT,
            user_id integer,
            text varchar,
            author varchar,
            title varchar,
            url varchar,
            post_time varchar,
            last_updated_time varchar,
            FOREIGN KEY (user_id) REFERENCES users(user_id))"""
    c.execute(query)
    query = """CREATE TABLE IF NOT EXISTS comments(
            comment_id integer PRIMARY KEY AUTOINCREMENT,
            user_id integer,
            article_id integer,
            display_name varchar,
            comment varchar,
            post_time varchar,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (article_id) REFERENCES articles(article_id))"""
    c.execute(query)
    query = """CREATE TABLE IF NOT EXISTS tags(
            tag_id integer PRIMARY KEY AUTOINCREMENT,
            tag_name varchar,
            url varchar,
            post_time integer)"""
    c.execute(query)

    query = "PRAGMA foreign_keys = ON"
    c.execute(query)
    conn.commit()
