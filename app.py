from flask import Flask, render_template, request, redirect
from flask_cors import CORS
from os import system

app = Flask(__name__)
CORS(app)

with open('.num.txt', 'r') as num_file:
    read = num_file.read()
    num = int(read)


@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        with open('.num.txt', 'w') as write:
            write.write(str(num+1))

        system('touch ' + str(num+1) + '.html')

        model = open('model.html').read()
        model = model.replace('url', url)
        command = 'echo \'%s\' > %s'%(model, str(num+1))
        system(command)


    return render_template('index.html', path = 'https://cnmc.tw/s/' + str(num+1))

if __name__ == '__main__':
    app.run(host = '140.131.149.15', port = 8080, debug = True)
