import sqlite3 as sql

def trans(url, new_url):
    con = sql.connect("short.db")
    cur = con.cursor()
    cur.execute("")
    
    con.commit()
    con.close()
    
def get_page(url):
    con = sql.connect("short.db")
    cur = con.cursor()
    cur.execute("")
