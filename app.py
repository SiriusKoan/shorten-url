from flask import Flask, render_template, request
from flask_cors import CORS
from os import system, popen
from flask_recaptcha import ReCaptcha
from models import *
from string import ascii_letters, digits


app = Flask(__name__)
CORS(app)

public_key = "6Lc7UMUUAAAAAEVWlNxm5SNF7kaiixUZAVBoyNVc"
private_key = "6Lc7UMUUAAAAALl0APCC9dCjzKKOz0Cgys1K91q1"
app.config.update(dict(
    RECAPTCHA_ENABLED = True,
    RECAPTCHA_SITE_KEY = public_key,
    RECAPTCHA_SECRET_KEY = private_key,
))

recaptcha = ReCaptcha()
recaptcha.init_app(app)

allow = ascii_letters + digits + '_-\\'


@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', path = '')
    elif request.method == 'POST':
        if recaptcha.verify():
            url = request.form.get('url')
            new_url = request.form.get('new-url')

            if not all(ch in allow for ch in new_url):
                return "New URL not allowed..."
                      
            trans(request.remote_addr, url, new_url)

            model = open('model.js').read()
            model = model.replace('url', url)
            command = 'touch ../s/' + new_url + ' && echo \'%s\' > ../s/%s'%(model, new_url)
            system(command)

            return 'https://cnmc.tw/s/' + new_url
        else:
            ###################print(request.path)
            return '<h1 style="color: red;">please verify</h1><br><a href="/">back home</a>'


@app.errorhandler(404)
def redirect(e):
    page = get_page(request.path)
    model = open('model.html').read()
    model = model.replace('url', page)
    return model

                       
if __name__ == '__main__':
    app.run(host = '127.0.0.1', port = 8080, debug = True)
