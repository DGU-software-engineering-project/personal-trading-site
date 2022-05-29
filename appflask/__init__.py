from flask import Flask,render_template,redirect,request, url_for, abort,session,flash,jsonify
from platformdirs import user_config_dir
import pymongo
from bson.objectid import ObjectId
from bson.json_util import loads, dumps
from werkzeug.utils import secure_filename
import os
app = Flask(__name__)
app.debug = True
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
    return render_template('index.html', entries=entries, user = usr)

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
@app.route('/file_upload', methods = ['POST'])
def file_upload():
    if 'file' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        return resp
    files = request.files.getlist('file')
    success = False

    for f in files:
        filename =secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        success = True
    if success:
        resp = jsonify({'message':'File successfully uploaded'})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify({'message':'error'})
        resp.status_code = 400
        return resp
# follow API
@app.route('/follow/<userid>', methods = ['POST'])
def file_upload(userid):
    if not session['ID']:
        resp = jsonify({'message': 'sign in first'})
        resp.status_code = 400
        return resp
    else:
        users.update_one({'ID': session['ID']},{'$push':{'FOLLOWING':user_config_dir}})
        resp = jsonify({'message':'Success Follow'})
        resp.status_code = 201
        return resp
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
@app.route('/mypage/<userid>', methods = ['GET', 'POST'])
def mypage(userid):
    tmp = items.find({"ID": userid})
    return render_template('mypage.html',iteminfo=tmp)

@app.route('/item_register', methods = ['GET', 'POST'])
def item_register():
    if request.method == 'POST':
        name=request.form['productName']
        price=request.form['productPrice']
        explain=request.form['productExplain']
        dic = {"item" :name, "price" :price, "sold" :False, "ID":session['ID'],"explain" :explain}
        items.insert_one(dic)
        return redirect(url_for('mypage',userid=session['ID']))
    return render_template('item_register.html')

@app.route('/item_edit/<itemid>', methods = ['GET', 'POST'])
def item_edit(itemid):
    tmp = items.find_one({'_id': ObjectId(itemid)})
    if request.method == 'POST':
        name=request.form['productName']
        price=request.form['productPrice']
        explain=request.form['productExplain']
        dic = {"item" :name, "price" :price, "sold" :False, "ID":session['ID'],"explain" :explain}
        items.update_one({'_id': ObjectId(itemid)},{"$set":dic})
        return redirect(url_for('mypage',userid=session['ID']))
    return render_template('item_edit.html',iteminfo = tmp)

if __name__ == '__main__':
    app.run()



