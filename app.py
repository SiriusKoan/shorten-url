from flask import Flask, render_template, request
from flask_cors import CORS
from os import system, popen
from flask_recaptcha import ReCaptcha
from models import *
from string import ascii_letters, digits
import config


app = Flask(__name__)
CORS(app)

app.config.update(dict(
    RECAPTCHA_ENABLED = True,
    RECAPTCHA_SITE_KEY = config.public_key,
    RECAPTCHA_SECRET_KEY = config.private_key,
))

recaptcha = ReCaptcha()
recaptcha.init_app(app)

allow = ascii_letters + digits + '_-\\'


@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        if recaptcha.verify():
            url = request.form.get('url')
            new_url = request.form.get('new-url')

            if not (all(ch in allow for ch in new_url) and new_url != ""):
                return render_template("char-forbidden.html")
            if new_url in ["new", "old", "who", "id"]:
                return render_template("string-forbidden.html")
            
            if not check(new_url):
                return "This short url has been occupied..."

            trans(request.remote_addr, url, new_url)

            return "<script>alert('https://cnmc.tw/%s')</script>"%new_url
        else:
            return render_template("verify-error.html")




if __name__ == '__main__':
    app.run(host = '127.0.0.1', port = 8080, debug = True)
