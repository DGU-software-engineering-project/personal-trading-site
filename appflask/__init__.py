from flask import Flask,render_template,redirect,request, url_for, abort,session,flash
import pymongo
from bson.objectid import ObjectId
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
    usr = list(users.find())
    return render_template('index.html', entries=entries, users = usr)
# API들
# user 목록 API
@app.route('/users')
def viewusers():
    tmp = users.find()
    return dumps(tmp)
# 전체 item 목록 API
@app.route('/items')
def viewitems():
    tmp = items.find()
    return dumps(tmp)
# 사진 불러오는 API
@app.route('/static/<photo>')
def viewphoto(photo):
    return render_template('img.html', image_file='images/'+photo)
# user 별 item 목록 API
@app.route('/items/<userid>')
def viewuseritems(userid):
    tmp = items.find({"ID": userid})
    return dumps(tmp)
# logout API
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
# file upload API
@app.route('/file_upload', methods = ['GET', 'POST'])
def file_upload():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],f.filename))
    return redirect(url_for('item_register'))
# 여기서부터 페이지들
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

# itemspec/item의 objectid
@app.route('/itemspec/<itemid>')
def viewitemspec(itemid):
    tmp = items.find_one({'_id': ObjectId(itemid)})
    return render_template('item_spec.html',iteminfo = tmp)
@app.route('/mypage', methods = ['GET', 'POST'])
def mypage():
    return render_template('mypage.html')

@app.route('/item_register', methods = ['GET', 'POST'])
def item_register():
    if request.method == 'POST':
        name=request.form['productName']
        price=request.form['prodentPrice']
        explain=request.form['productExplain']
        dic = {"item" :name, "price" :price, "sold" :False, "ID":session['ID'],"explain" :explain}
        items.insert_one(dic)
        redirect(url_for('mypage'))
    return render_template('item_register.html')

@app.route('/item_edit/<itemid>', methods = ['GET', 'POST'])
def item_edit(itemid):
    tmp = items.find_one({'_id': ObjectId(itemid)})
    if request.method == 'POST':
        name=request.form['productName']
        price=request.form['prodentPrice']
        explain=request.form['productExplain']
        dic = {"item" :name, "price" :price, "sold" :False, "ID":session['ID'],"explain" :explain}
        items.update_one({'_id': ObjectId(itemid)},{"$set":dic})
        redirect(url_for('mypage'))
    return render_template('item_edit.html',iteminfo = tmp)

if __name__ == '__main__':
    app.run(debug=True)



