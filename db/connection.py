import mariadb
from db.config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME


_connection = None


def get_connection():
    global _connection
    if _connection is None:
        _connection = mariadb.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            autocommit=True,
        )
        cur = _connection.cursor()
        cur.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` CHARACTER SET utf8mb4;")
        cur.execute(f"USE `{DB_NAME}`;")
        cur.close()
    return _connection
