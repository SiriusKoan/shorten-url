from flask import Flask, render_template, request
from flask_cors import CORS
from os import system, popen

app = Flask(__name__)
CORS(app)

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
