import sqlite3 as sql

def check(new_url):
    con = sql.connect("short.db")
    cur = con.cursor()
    cur.execute("SELECT old from short where new=(url) VALUES (?)", (new_url))
    check = cur.fetchall()
    if check != [('')]: #
        retunr "This short url has been occupied..."
    
def trans(ip, url, new_url):
    con = sql.connect("short.db")
    cur = con.cursor()
    cur.execute("INSERT INTO short (who, old, new) VALUES (?, ?, ?)", (ip, url, new_url))
    con.commit()
    con.close()
    
def get_page(url):
    con = sql.connect('short.db')
    cur = con.cursor()
    cur.execute('SELECT old FROM short WHERE new="%s"'%(url[1:]))
    new = cur.fetchall()
    con.close()
    return new[0][0]    # new_url
