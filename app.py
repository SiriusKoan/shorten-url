from flask import Flask, render_template, request
from flask_cors import CORS
from os import system, popen
from flask_recaptcha import ReCaptcha


app = Flask(__name__)
CORS(app)

app.config.update(dict(
    RECAPTCHA_ENABLED = True,
    RECAPTCHA_SITE_KEY = "6Lc7UMUUAAAAAEVWlNxm5SNF7kaiixUZAVBoyNVc",
    RECAPTCHA_SECRET_KEY = "6Lc7UMUUAAAAALl0APCC9dCjzKKOz0Cgys1K91q1",
))

recaptcha = ReCaptcha()
recaptcha.init_app(app)

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', path = '')
    if request.method == 'POST':
        if recaptcha.verify():
            url = request.form.get('url')
            new_url = request.form.get('new-url')
            if new_url in popen("ls ../s").read().split('\n'):
                return 'this url has been occurpied...<a href="/">back home</a>'

            model = open('model.html').read()
            model = model.replace('url', url)
            command = 'touch ../s/' + new_url + '&& echo \'%s\' > ../s/%s'%(model, new_url)
            system(command)

            return render_template('index.html', path = 'https://cnmc.tw/s/' + new_url)
        else:
            return '<h1 style="color: red;">please verify</h1><br><a href="/">back home</a>'

if __name__ == '__main__':
    app.run(host = '127.0.0.1', port = 8080, debug = True)
