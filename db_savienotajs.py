import sqlite3
import sys

def izveidot_savienojumu():
    try:
        conn = sqlite3.connect("konkurss.db")
        conn.row_factory = sqlite3.Row
        parbaudit = conn.execute("SELECT * FROM pieteikumi")
        return conn
    except sqlite3.OperationalError:
        sys.exit("Kļūda. Datubāze nav atrasta vai bojāta tās struktūra.")

def slegt_savienojumu(conn):
    conn.commit()
    conn.close()

izveidot_savienojumu()