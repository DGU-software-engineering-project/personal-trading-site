#from flask import Flask, g, Response, make_response
from flask import Flask, render_template, request, redirect, url_for, abort, session

app = Flask(__name__)
app.debug = True

app.secret_key = 'software_engineering'


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/signup', methods = ['GET', 'POST'])
def sign_up():
    return render_template('sign_up.html')
        
@app.route('/item', methods = ['GET', 'POST'])
def item():
    return render_template('item_spec.html')
        
if __name__ == '__main__':
    app.run()