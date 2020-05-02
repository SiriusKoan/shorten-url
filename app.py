from flask import Flask, render_template, request
from flask_cors import CORS
from os import system, popen
from flask_recaptcha import ReCaptcha
from models import *
from string import ascii_letters, digits
import config
import datetime


app = Flask(__name__)
CORS(app)

app.config.update(dict(
    RECAPTCHA_ENABLED = True,
    RECAPTCHA_SITE_KEY = config.recaptcha_public_key,
    RECAPTCHA_SECRET_KEY = config.recaptcha_private_key,
))

recaptcha = ReCaptcha()
recaptcha.init_app(app)

allow = ascii_letters + digits + '_-'


@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        if recaptcha.verify():
            url = request.form.get('url')
            new_url = request.form.get('new-url')

            if not (all(ch in allow for ch in new_url) and new_url != ""):
                return 'Error', 400
            if new_url in ["new", "old", "who", "id"]:
                return 'Error', 400
            if not check(new_url):
                return "This short url has been occupied..."

            save(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), request.remote_addr, url, new_url)

            return "<script>alert('https://cnmc.tw/%s');window.location.replace('/');</script>"% new_url
        else:
            return 'Error', 400


@app.route('/api', methods = ['POST'])
def api():
    payload = request.get_json()
    old_url = payload['old_url']
    new_url = payload['new_url']

@app.errorhandler(404)
def redirect(e):
    try:
        to_url = get_page(request.path)
    except:
        return 404
    else:
        return render_template('redirect.html', to_url = to_url)

if __name__ == '__main__':
    app.run(host = '127.0.0.1', port = 8080, debug = True)
