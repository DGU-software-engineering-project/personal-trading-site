#from flask import Flask, g, Response, make_response
from flask import Flask, render_template, request, redirect, url_for, abort, session

app = Flask(__name__)
app.debug = True

app.secret_key = 'software_engineering'


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods == ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        id = request.form['id']
        pw = request.form['pw']
        


if __name__ == '__main__':
    app.run()