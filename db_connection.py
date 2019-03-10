import sqlite3

database = '/Users/saketgonte/Desktop/Projects/twitter/twitter.db'


def get_db():
    db = sqlite3.connect(database)
    return db


def create_tables():
    conn = get_db()
    c = conn.cursor()
    query = """CREATE TABLE IF NOT EXISTS users(
            username VARCHAR(50) PRIMARY KEY,
            password VARCHAR(50),
            display_name VARCHAR(50))"""
    c.execute(query)
    query = """CREATE TABLE IF NOT EXISTS articles(
            text VARCHAR(200),
            title VARCHAR(50),
            author VARCHAR(50),
            created_time INTEGER,
            last_updated_time INTEGER)"""
    c.execute(query)
    conn.commit()
