import sqlite3

conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    username TEXT PRIMARY KEY,
    password TEXT
)
""")

conn.commit()


def register(username, password):

    try:

        cursor.execute(
            "INSERT INTO users VALUES(?, ?)",
            (username, password)
        )

        conn.commit()

        return True

    except:

        return False


def login(username, password):

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    return cursor.fetchone()