import sqlite3 as sql

def trans(ip, url, new_url):
    con = sql.connect("short.db")
    cur = con.cursor()
    cur.execute("INSERT INTO short (who, old, new) VALUES (?, ?, ?)", (ip, url, new_url))
    con.commit()
    con.close()
    
def get_page(url):
    con = sql.connect('short.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM short WHERE old="%s"'%url)
    new = cur.fetchall()
    con.close()
    return new[0][3]    # new_url
