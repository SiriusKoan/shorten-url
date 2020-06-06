import sqlite3 as sql
from re import fullmatch

def occupy(new_url):
    con = sql.connect("data.db")
    cur = con.cursor()
    cur.execute("SELECT old from urls where new = ?", (new_url,))
    check = cur.fetchall()
    if len(check) > 0:
        return False
    return True

def check(new_url):
    if fullmatch('[a-zA-Z0-9_-]+', new_url) and new_url not in ["new", "old", "who", "id"] and occupy(new_url):
        return True
    return False

def save(time, ip, url, new_url):
    con = sql.connect("data.db")
    cur = con.cursor()
    cur.execute("INSERT INTO urls (insert_time, who, old, new) VALUES (?, ?, ?, ?)", (time, ip, url, new_url,))
    con.commit()
    con.close()
    
def get_page(url):
    con = sql.connect('data.db')
    cur = con.cursor()
    cur.execute('SELECT old FROM urls WHERE new = ?', (url[1:],))
    new = cur.fetchone()
    con.close()
    return new[0]    # new_url
