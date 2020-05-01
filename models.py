import sqlite3 as sql

def check(new_url):
    con = sql.connect("short.db")
    cur = con.cursor()
    cur.execute("SELECT old from short where new=?", (new_url,))
    check = cur.fetchall()
    if len(check) > 0:
        return "This short url has been occupied..."
    
def trans(ip, url, new_url):
    con = sql.connect("short.db")
    cur = con.cursor()
    cur.execute("INSERT INTO short (who, old, new) VALUES (?, ?, ?)", (ip, url, new_url,))
    con.commit()
    con.close()
    
def get_page(url):
    con = sql.connect('short.db')
    cur = con.cursor()
    cur.execute('SELECT old FROM short WHERE new=?', (url[1:],))
    new = cur.fetchone()
    con.close()
    return new[0]    # new_url
