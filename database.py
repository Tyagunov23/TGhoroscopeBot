import sqlite3

DB_PATH = 'bot_users.db'


def get_connection():
    return sqlite3.connect(DB_PATH)


def initialize_database():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            zodiac_sign TEXT,
            subscribed INTEGER DEFAULT 1,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        conn.commit()


def add_user(user_id, username=None, zodiac_sign=None):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM users WHERE id = ?", (user_id,))
        if cursor.fetchone() is None:
            cursor.execute(
                "INSERT INTO users (id, username, zodiac_sign) VALUES (?, ?, ?)",
                (user_id, username, zodiac_sign)
            )
        else:
            cursor.execute(
                "UPDATE users SET zodiac_sign = ?, subscribed = 1 WHERE id = ?",
                (zodiac_sign, user_id)
            )
        conn.commit()


def get_subscribed_users():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, zodiac_sign FROM users WHERE subscribed = 1")
        return cursor.fetchall()


def update_subscription(user_id, subscribe=True):
    with get_connection() as conn:
        cursor = conn.cursor()
        status = 1 if subscribe else 0
        cursor.execute("UPDATE users SET subscribed = ? WHERE id = ?", (status, user_id))
        conn.commit()


def delete_user(user_id):
    """
    Удаляет пользователя из базы данных по его ID.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
