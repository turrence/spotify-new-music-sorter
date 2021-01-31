import sqlite3
import os

from constant import CACHE_PATH, DATABASE_NAME
# utility functions for manipulating the database
# aka abstracting away all the sql

def get_user(id):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM Users WHERE id="{id}"')
    conn.commit()
    conn.close()
    return cursor.fetchone()

def update_user(id, field, value):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(f'UPDATE Users SET {field}="{value}" WHERE id="{id}"')
    conn.commit()
    conn.close()

def get_field(id, field):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(f'SELECT {field} FROM Users WHERE id = "{id}"')
    entry = cursor.fetchone()[0]
    update_user(id, field, entry + 1)
    conn.close()
    return entry

def increment_field(id, field):
    entry = get_field(id, field)
    update_user(id, field, entry + 1)

def add_user(id):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    conn.execute(f'INSERT INTO Users(id) VALUES("{id}")')
    conn.commit()
    conn.close()

def remove_user(id):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    conn.execute(f'DELETE FROM Users WHERE id = "{id}"')
    conn.commit()
    conn.close()

def init_database():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Users' ''')
    if cursor.fetchone()[0] == 0:
        conn.execute(''' CREATE TABLE Users(
            id TEXT,
            update_count INTEGER DEFAULT 0,
            error_count INTEGER DEFAULT 0,
            last_error TEXT DEFAULT "",
            last_playlist TEXT DEFAULT "",
            last_update TEXT DEFAULT ""
        ) ''')
        for filename in os.listdir(CACHE_PATH):
            id = filename[len(".cache-"):]
            add_user(id)
    conn.close()
