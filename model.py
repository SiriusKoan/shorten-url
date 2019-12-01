import sqlite3 as sql

def trans():
    con = sql.connect("short.db")
    cur = con.cursor()
