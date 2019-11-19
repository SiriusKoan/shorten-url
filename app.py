from flask import Flask, render_template, request, redirect
from flask_cors import CORS
from os import system

app = Flask(__name__)
CORS(app)

file = open('.num.txt', 'r')
num = file.read()
num = int(num)
file.close()
@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = open('.num.txt', 'w')
        file.write(str(num+1))
        url = request.form.get('url')
        system('touch ' + str(num+1) + '.html')
        model = open('model.html').read()
        model = model.replace('url', url)
        command = 'echo \'%s\' > %s'%(model, str(num+1))
        system(command)
        file.close()


    return render_template('index.html', path = 'https://cnmc.tw/s/' + str(num+1))

if __name__ == '__main__':
    app.run(host = '140.131.149.15', port = 8080, debug = True)
