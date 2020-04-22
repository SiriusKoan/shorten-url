# shorten-url
<img src="https://img.shields.io/badge/testing-red"></img>
## setup
1. Create a database named short.db.
```sh
$ sudo sqlite3 short.db < schema.sql
```
## deploy
Run app.py. You can modify the port and IP address.
```sh
$ sudo flask run --port 8080 --host 127.0.0.1
```
