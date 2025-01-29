import logging
import os
import sqlite3
from typing import Optional


DATABASE_PATH = os.path.join("data", "data.db")
logger = logging.getLogger("bot")


def create_database() -> None:
    create_dir()

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


def create_dir() -> None:
    dir_name = os.path.dirname(DATABASE_PATH)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name, exist_ok=True)


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
                   "first_name TEXT DEFAULT NULL,"
                   "last_name TEXT DEFAULT NULL,"
                   "date_of_birth TIMESTAMP DEFAULT NULL,"
                   "gender TEXT DEFAULT NULL,"
                   "age_min INT DEFAULT NULL,"
                   "age_max INT DEFAULT NULL,"
                   "biography TEXT DEFAULT NULL)")


def check_if_user_registered(user_tg_id: int) -> bool:
    """
    :param user_tg_id: user ID in Telegram.
    :return: True if user was registered.
    """

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT user_tg_id FROM users WHERE user_tg_id = ?", (user_tg_id, ))
    user = cursor.fetchone()
    conn.close()
    return user is not None


def get_photo(user_tg_id: int) -> Optional[bytes]:
    """
    :param user_tg_id: user ID in Telegram.
    :return: photo of user.
    """

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT photo FROM photos WHERE user_tg_id = ?", (user_tg_id,))
    photo = cursor.fetchone()
    conn.close()
    if photo is not None:
        photo = photo[0]
    return photo


def register_user(user_tg_id: int, username: str) -> None:
    """
    :param user_tg_id: user ID in Telegram;
    :param username: username in Telegram.
    """

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (user_tg_id, username) VALUES (?, ?)", (user_tg_id, username))
    conn.commit()
    conn.close()


def save_user_photo(user_tg_id: int, photo: bytes) -> None:
    """
    :param user_tg_id: user ID in Telegram;
    :param photo: new user photo.
    """

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO photos (id, photo, user_tg_id) VALUES (NULL, ?, ?)", (photo, user_tg_id))
    conn.commit()
    conn.close()


def update_user_photo(user_tg_id: int, photo: bytes) -> None:
    """
    :param user_tg_id: user ID in Telegram;
    :param photo: new user photo.
    """

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE photos SET photo = ? WHERE user_tg_id = ?", (photo, user_tg_id))
    conn.commit()
    conn.close()
