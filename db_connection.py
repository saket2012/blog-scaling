import sqlite3

users_db = 'users.db'
articles_db = 'articles.db'
tags_db = 'tags.db'
comments_db = 'comments.db'


def get_db_users():
    db = sqlite3.connect(users_db)
    return db


def get_db_articles():
    db = sqlite3.connect(articles_db)
    return db


def get_db_tags():
    db = sqlite3.connect(tags_db)
    return db


def get_db_comments():
    db = sqlite3.connect(comments_db)
    return db


def create_tables():
    conn_users = get_db_users()
    c_users = conn_users.cursor()
    query = """CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username varchar UNIQUE,
            password varchar,
            display_name varchar)"""
    c_users.execute(query)

    conn_articles = get_db_articles()
    c_articles = conn_articles.cursor()
    query = """CREATE TABLE IF NOT EXISTS articles(
            article_id integer PRIMARY KEY AUTOINCREMENT,
            username varchar,
            text varchar,
            author varchar,
            title varchar,
            url varchar,
            post_time varchar,
            last_updated_time varchar)"""
    c_articles.execute(query)

    conn_comments = get_db_comments()
    c_comments = conn_comments.cursor()
    query = """CREATE TABLE IF NOT EXISTS comments(
            comment_id integer PRIMARY KEY AUTOINCREMENT,
            username varchar,
            article_id integer,
            comment varchar,
            post_time varchar)"""
    c_comments.execute(query)

    conn_tags = get_db_tags()
    c_tags = conn_tags.cursor()
    query = """CREATE TABLE IF NOT EXISTS tags(
            tag_id integer PRIMARY KEY AUTOINCREMENT,
            username varchar,
            tag_name varchar,
            url varchar,
            post_time varchar)"""
    c_tags.execute(query)
