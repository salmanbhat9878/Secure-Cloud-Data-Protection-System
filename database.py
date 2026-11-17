import sqlite3
from pathlib import Path

# Always use the database inside this project folder
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "security.db"
print("DATABASE LOCATION:", DB_PATH)


def get_connection():
    return sqlite3.connect(str(DB_PATH))


def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            encrypted_data BLOB NOT NULL
        )
    """)

    # Access tokens table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS access_tokens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            token_hash TEXT NOT NULL
        )
    """)

    # Activity logs table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS activity_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            activity TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_table()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT username FROM users")
    print("Registered Users:", cursor.fetchall())

    conn.close()