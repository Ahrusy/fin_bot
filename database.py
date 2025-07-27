# database.py
import sqlite3

conn = sqlite3.connect("user.db")
cursor = conn.cursor()

def init_db():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            telegram_id INTEGER UNIQUE,
            name TEXT,
            category1 TEXT,
            category2 TEXT,
            category3 TEXT,
            expenses1 REAL,
            expenses2 REAL,
            expenses3 REAL
        )
    ''')
    conn.commit()

def get_user(telegram_id):
    cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
    return cursor.fetchone()

def register_user(telegram_id, name):
    cursor.execute("INSERT INTO users (telegram_id, name) VALUES (?, ?)", (telegram_id, name))
    conn.commit()

def save_finances(telegram_id, data):
    cursor.execute('''
        UPDATE users SET
            category1 = ?, expenses1 = ?,
            category2 = ?, expenses2 = ?,
            category3 = ?, expenses3 = ?
        WHERE telegram_id = ?
    ''', (
        data['category1'], data['expenses1'],
        data['category2'], data['expenses2'],
        data['category3'], data['expenses3'],
        telegram_id
    ))
    conn.commit()
