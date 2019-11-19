from flask import Flask, render_template, request
from flask_cors import CORS
from os import system

app = Flask(__name__)
CORS(app)

with open(r'.num.txt') as num_file:
    read = num_file.read()
    num = int(read)

@app.route('/', methods = ['GET', 'POST'])
def index():
    global num
    num = num + 1
    if request.method == 'GET':
        return render_template('index.html', path = '')
    if request.method == 'POST':
        url = request.form.get('url')
        with open(r'.num.txt', 'w') as write:
            write.write(str(num))

        system('touch ' + str(num) + '.html')

        model = open('model.html').read()
        model = model.replace('url', url)
        command = 'echo \'%s\' > %s'%(model, str(num))
        system(command)

        return render_template('index.html', path = 'https://cnmc.tw/s/' + str(num))

if __name__ == '__main__':
    app.run(host = '127.0.0.1', port = 8080, debug = True)
