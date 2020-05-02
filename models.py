import sqlite3 as sql

def check(new_url):
    con = sql.connect("data.db")
    cur = con.cursor()
    cur.execute("SELECT old from urls where new = ?", (new_url,))
    check = cur.fetchall()
    print(check)
    if len(check) > 0:
        return False
    return True
    
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
