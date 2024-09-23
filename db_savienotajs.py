import sqlite3
import sys

def izveidot_savienojumu():
    try:
        conn = sqlite3.connect("konkurss.db")
        conn.row_factory = sqlite3.Row
        return conn
    except:
        sys.exit("Kļūda. Datubāze nav atrasta.")

def slegt_savienojumu(conn):
    conn.commit()
    conn.close()
