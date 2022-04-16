import sqlite3


def get_db_connection(db='database.db'):
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    return conn


def get_db_cursor(conn):
    return conn.cursor()


def execute_query(conn, query, args=None):
    cursor = get_db_cursor(conn)
    if args:
        cursor.execute(query, args)
    else:
        cursor.execute(query)
    conn.commit()
    return cursor


def execute_many(conn, query, args):
    cursor = get_db_cursor(conn)
    cursor.executemany(query, args)
    return cursor
