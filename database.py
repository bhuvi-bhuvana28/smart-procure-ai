import sqlite3
from datetime import datetime
import pandas as pd


def create_table():

    conn = sqlite3.connect("logs.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS procurement_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            best_vendor TEXT,
            score REAL,
            timestamp TEXT
        )
        """
    )

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
            float(score),
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )
    )

    conn.commit()
    conn.close()


def get_logs():

    conn = sqlite3.connect("logs.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM procurement_logs
        ORDER BY id DESC
        """
    )

    rows = cursor.fetchall()

    conn.close()

    return rows


def get_logs_dataframe():

    conn = sqlite3.connect("logs.db")

    df = pd.read_sql_query(
        """
        SELECT *
        FROM procurement_logs
        ORDER BY id DESC
        """,
        conn
    )

    conn.close()

    return df


def delete_logs():

    conn = sqlite3.connect("logs.db")

    cursor = conn.cursor()

    cursor.execute(
    "DELETE FROM procurement_logs"
    )

    conn.commit()
    conn.close()