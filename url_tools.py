from re import fullmatch
import datetime
from database import db, URLs


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