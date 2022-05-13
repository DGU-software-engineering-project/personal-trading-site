from flask import Flask,render_template,redirect,request
import pymongo
from bson.json_util import loads, dumps
app = Flask(__name__)
client = pymongo.MongoClient("mongodb+srv://admin:1234@cluster0.il12x.mongodb.net/tradingSiteDB?retryWrites=true&w=majority")
db = client['tradingSiteDB']
users = db.usersDB
items = db.itemsDB

@app.route('/')
def home():
    entries = list(items.find())
    return render_template('home.html', entries=entries)

@app.route('/users')
def viewusers():
    tmp = users.find()
    return dumps(tmp)

# @app.route('/signin',methods = ['POST', 'GET'])
# def login():
#     if request.method == 'POST':
#         if request.form['profName'] in users.find():
#             return redirect(url_for('success'))
#         else:
#             abort(401)
#     else:
#         return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)