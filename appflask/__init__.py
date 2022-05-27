from flask import Flask,render_template,redirect,request, url_for, abort,session,flash
import pymongo
from bson.json_util import loads, dumps
from werkzeug.utils import secure_filename
import os
app = Flask(__name__)
client = pymongo.MongoClient("mongodb+srv://admin:1234@cluster0.il12x.mongodb.net/tradingSiteDB?retryWrites=true&w=majority")
db = client['tradingSiteDB']
users = db.usersDB
items = db.itemsDB
app.config.update(SECRET_KEY='secret')
app.config['UPLOAD_FOLDER'] = './personal-trading-site/appflask/static/images'
@app.route('/')
def index():
    entries = list(items.find())
    return render_template('index.html', entries=entries)

@app.route('/followees')
def viewusers():
    if 'ID' in session:
        tmp = users.find_one({'ID': session['ID']},{'FOLLOWING':1})
        return dumps(tmp)
    return "login first"
    
@app.route('/items')
def viewitems():
    tmp = items.find()
    return dumps(tmp)
@app.route('/items/<userid>')
def viewuseritems(userid):
    tmp = items.find({"ID": userid})
    return dumps(tmp)
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
@app.route('/file_upload', methods = ['GET', 'POST'])
def file_upload():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],f.filename))
    return redirect(url_for('item_register'))

@app.route('/signin',methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        id=request.form['loginid']
        pw=request.form['loginpw']
        userinfo = users.find_one({"ID" :id})
        if userinfo:
            if userinfo["PW"] == pw:
                session['ID']=id
                return redirect(url_for('index'))
            else:
                return "password incorrect"
        else:
            return "Id incorrect"
    else:
        return render_template('signin.html')

@app.route('/signup', methods = ['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        id=request.form['loginid']
        pw=request.form['loginpw']
        name=request.form['name']
        userdic = {"name":name,"ID":id,"PW":pw, "FOLLOWING":[]}
        users.insert_one(userdic)
        flash('signup success')
        return redirect(url_for('index'))
    else:
        return render_template('sign_up.html')

@app.route('/item', methods = ['GET', 'POST'])
def item():
    return render_template('item_spec.html')

@app.route('/mypage', methods = ['GET', 'POST'])
def mypage():
    return render_template('mypage.html')

@app.route('/item_register', methods = ['GET', 'POST'])
def item_register():
    if request.method == 'POST':
        name=request.form['productName']
        price=request.form['prodentPrice']
        explain=request.form['productExplain']
    return render_template('item_register.html')

@app.route('/item_edit', methods = ['GET', 'POST'])
def item_edit():
    return render_template('item_edit.html')

if __name__ == '__main__':
    app.run(debug=True)



