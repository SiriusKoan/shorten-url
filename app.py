from flask import Flask, render_template, request
from flask_cors import CORS
from os import system, popen
from form import trans
from flask_wtf import RecaptchaField, Form


app = Flask(__name__)
CORS(app)

app.config['RECAPTCHA_PUBLIC_KEY'] = '6LdTFsUUAAAAAATO4ICHeRhknaXNNQEqOMqwejsz'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LdTFsUUAAAAANEw_EpSUi5MQ539a5kL_ffKs07m'
app.config['SECRET_KEY'] = 'youdontknow'
app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_OPTIONS'] = {'theme':'black'}

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', path = '')
    if request.method == 'POST':
        url = request.form.get('url')
        new_url = request.form.get('new-url')
        if new_url in popen("ls ../s").read().split('\n'):
            return 'this url has been occurpied...<a href="/">back home</a>'

        model = open('model.html').read()
        model = model.replace('url', url)
        command = 'touch ../s/' + new_url + '&& echo \'%s\' > ../s/%s'%(model, new_url)
        system(command)

        return render_template('index.html', path = 'https://cnmc.tw/s/' + new_url)

if __name__ == '__main__':
    app.run(host = '127.0.0.1', port = 8080, debug = True)
