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
        userinfo = users.find_one({"ID" :request.form['loginid']})
        if userinfo:
            if userinfo["PW"] == request.form['loginpw']:
                session['ID']=request.form['loginid']
                return render_template('home.html',isLoggedin=True, username=request.form['loginid'])
            else:
                return "password incorrect"
        else:
            return "Id incorrect"
    else:
        return render_template('signin.html')

if __name__ == '__main__':
    app.run(debug=True)