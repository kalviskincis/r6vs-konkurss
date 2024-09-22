import sqlite3
import sys

konkurss = "konkurss.db"

def izveidot_savienojumu(*arg):
    try:
        conn = sqlite3.connect(arg[0])
        conn.row_factory = sqlite3.Row
        print(conn)
        return conn
    except:
        sys.exit("Kļūda. Datubāze nav atrasta.")

def slegt_savienojumu(conn):
    conn.commit()
    conn.close()
