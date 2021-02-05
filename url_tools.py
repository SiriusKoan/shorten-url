from re import fullmatch
import datetime
from database import db, URLs
from pygal import Pie


def add_url(old, new, username, from_ip):
    if (
        fullmatch("[a-zA-Z0-9_-]+", new)
        and URLs.query.filter_by(new=new).first() is None
    ):
        new_url = URLs(
            insert_time=datetime.datetime.now(),
            username=username,
            from_ip=from_ip,
            old=old,
            new=new,
        )
        db.session.add(new_url)
        db.session.commit()
        return True
    else:
        return False
    
def get_urls_info(username):
    urls = URLs.query.filter_by(username=username).all()
    urls = [[url.insert_time.strftime("%Y/%m/%d"), url.from_ip, url.old, url.new, url.use] for url in urls]
    graph = draw_use_graph([[url[3], url[4]] for url in urls]) # only url.new and url.use
    return urls, graph

def draw_use_graph(urls):
    pie = Pie(inner_radius=0.4)
    pie.title = "Short URLs Use"
    for url in urls:
        pie.add(url[0], url[1])
    return pie.render_data_uri()
    
