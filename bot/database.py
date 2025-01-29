import logging
import os
import sqlite3


DATABASE_PATH = os.path.join("data", "data.db")
logger = logging.getLogger("bot")


def create_database() -> None:
    conn = sqlite3.connect(DATABASE_PATH, uri=True)
    cursor = conn.cursor()

    create_users_table(cursor)
    conn.commit()

    create_photos_table(cursor)
    conn.commit()

    create_likes_table(cursor)
    conn.commit()

    create_messages_table(cursor)
    conn.commit()

    conn.close()
    logger.info("Tables were created")


def create_likes_table(cursor) -> None:
    cursor.execute("CREATE TABLE IF NOT EXISTS likes("
                   "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                   "like INTEGER,"
                   "who_chose INTEGER,"
                   "who_was_chosen INTEGER,"
                   "FOREIGN KEY (who_chose) REFERENCES users (user_tg_id) ON DELETE CASCADE,"
                   "FOREIGN KEY (who_was_chosen) REFERENCES users (user_tg_id) ON DELETE CASCADE)")


def create_messages_table(cursor) -> None:
    cursor.execute("CREATE TABLE IF NOT EXISTS messages("
                   "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                   "date TIMESTAMP,"
                   "message TEXT,"
                   "from_user INTEGER,"
                   "to_user INTEGER,"
                   "FOREIGN KEY (from_user) REFERENCES users (user_tg_id) ON DELETE CASCADE,"
                   "FOREIGN KEY (to_user) REFERENCES users (user_tg_id) ON DELETE CASCADE)")


def create_photos_table(cursor) -> None:
    cursor.execute("CREATE TABLE IF NOT EXISTS photos("
                   "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                   "photo BLOB,"
                   "user_tg_id INTEGER,"
                   "FOREIGN KEY (user_tg_id) REFERENCES users (user_tg_id) ON DELETE CASCADE)")


def create_users_table(cursor) -> None:
    cursor.execute("CREATE TABLE IF NOT EXISTS users("
                   "user_tg_id INTEGER PRIMARY KEY,"
                   "username TEXT,"
                   "first_name TEXT,"
                   "last_name TEXT,"
                   "date_of_birth TIMESTAMP,"
                   "gender TEXT,"
                   "age_min INT,"
                   "age_max INT,"
                   "biography TEXT,"
                   "date TIMESTAMP)")
