import sqlite3
from datetime import datetime


def create_table():

    conn = sqlite3.connect("logs.db")

    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS procurement_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            best_vendor TEXT,
            score REAL,
            timestamp TEXT
        )
    ''')

    conn.commit()
    conn.close()



def insert_log(vendor, score):

    conn = sqlite3.connect("logs.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO procurement_logs
        (best_vendor, score, timestamp)
        VALUES (?, ?, ?)
        """,
        (
            vendor,
            score,
            str(datetime.now())
        )
    )

    conn.commit()
    conn.close()