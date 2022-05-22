from flask import Flask,render_template,redirect,request, url_for, abort,session
import pymongo
from bson.json_util import loads, dumps
app = Flask(__name__)
client = pymongo.MongoClient("mongodb+srv://admin:1234@cluster0.il12x.mongodb.net/tradingSiteDB?retryWrites=true&w=majority")
db = client['tradingSiteDB']
users = db.usersDB
items = db.itemsDB
app.config.update(SECRET_KEY='secret')
@app.route('/')
def home():
    entries = list(items.find())
    return render_template('home.html', entries=entries)

@app.route('/users')
def viewusers():
    tmp = users.find()
    return dumps(tmp)

@app.route('/items')
def viewitems():
    tmp = items.find()
    return dumps(tmp)
@app.route('/signin',methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        userinfo = users.find_one({"ID" :request.form['name']})
        if userinfo:
            if userinfo["PW"] == request.form['password']:
                session['ID']=request.form['name']
                return render_template('home.html',isLoggedin=True, username=request.form['name'])
            else:
                return "password incorrect"
        else:
            return "Id incorrect"
    else:
        return render_template('signin.html')

if __name__ == '__main__':
    app.run(debug=True)

#     from flask import Flask, render_template, request, redirect, url_for, abort, session

# app = Flask(__name__)
# app.debug = True

# app.secret_key = 'software_engineering'


# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/login', methods = ['GET', 'POST'])
# def login():
#     return render_template('login.html')

# @app.route('/signup', methods = ['GET', 'POST'])
# def sign_up():
#     return render_template('sign_up.html')
        
# @app.route('/item', methods = ['GET', 'POST'])
# def item():
#     return render_template('item_spec.html')

# @app.route('/mypage', methods = ['GET', 'POST'])
# def mypage():
#     return render_template('mypage.html')

# @app.route('/item_register', methods = ['GET', 'POST'])
# def item_register():
#     return render_template('item_register.html')

# @app.route('/item_edit', methods = ['GET', 'POST'])
# def item_edit():
#     return render_template('item_edit.html')

# if __name__ == '__main__':
#     app.run()