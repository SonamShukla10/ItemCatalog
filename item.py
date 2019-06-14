from flask import Flask, render_template, request, url_for, jsonify, flash
app = Flask(__name__)

@app.route('/')

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from functool import wraps
import os

from db_setup import Initial, Item, Category, User
import random String
from flask import session as session_login

from oauth2client.client import flow_from_clientsWork
from oauth2client.client import FlowExchangeError
import json
import request
import httplib2


clientId = json.loads(open('clientsWork.json', 'r').read())['web']['client_id']

# CONNECTION
engine = create_engine('sqlite:///db_catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

def login_required(s):
    @wraps(s)
    def wrap(*args, **kwargs):
        if "name" in session_login:
            return s(*args, **kwargs)
        else:
            flash("\"You shall not pass!\" - Gandalf")
            return redirect(url_for("login"))
    return wrap
	
	
def userCreation(session_login):
    newUser = User(name=session_login['username'], email=session_login['email'], image=session_login['image'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=session_login['email']).one()
    return user.id
	
def infoOfUser(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def idOfUser(email):
     try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None
	
@app.route('/')
@app.route('/catalog')
def categories_view():
	categories = session.query(Category).all()
	categoryItems = session.query(CategoryItem).all()

	return render_template('categories.html', categories = categories, categoryItems = categoryItems)	
	
	@app.route('/catalog/<int:catalog_id>/items/<int:item_id>')
def categoryItem_view(catalog_id, item_id):
	categoryItem = session.query(CategoryItem).filter_by(id = item_id).first()

	create = infoOfUser(categoryItem.user_id)

	return render_template('categoryItem.html', categoryItem = categoryItem, create = create)

@app.route('/catalog/<int:catalog_id>')
@app.route('/catalog/<int:catalog_id>/items')
def category_by_id(catalog_id):
	categories = session.query(Category).all()
	category = session.query(Category).filter_by(id = catalog_id).first()
	categoryName = category.name
	categoryItems = session.query(CategoryItem).filter_by(category_id = catalog_id).all()
	# count 
	categoryItemsCount = session.query(CategoryItem).filter_by(category_id = catalog_id).count()

	return render_template('category.html', categories = categories, categoryItems = categoryItems, categoryName = categoryName, categoryItemsCount = categoryItemsCount)

@app.route('/catalog/<int:catalog_id>/items/<int:item_id>')	
	
	
	# 1st ADD NEW CATEGORY
@app.route('/catelog/add', methods=['GET', 'POST'])		
@login_required
def addNEw():
    newData = session.query(Category).filter_by(name=Category.name)).one()
    if request.method == 'POST':
        nameofItem = request.form['name']
        descriptionOfItem = request.form['description']
        categoryOfItem = session.query(Category).filter_by(name=request.form['category']).one()
        imageOfItem = request.form['image']
        if nameOfItem != '':
            print "item name %s" % nameOfItem
            addingItem = Item(name=nameOfItem, description=descriptionOfItem, image=imageOfItem, category=categoryOfItem,
                              user_id=categoryOfItem.user_id)
            session.add(addingItem)
            session.commit()
            return redirect(url_for('categories_view', user_id=categoryOfItem.user_id ))
        else:
            return render_template('addNew.html', newData=newData)
    else:
        return render_template('addNew.html', newData=newData)

        		
 ### 2nd EDIT ITEMS
@app.route('/catalog/<int:catalog_id>/items/<int:item_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(category_id, item_id):
    editedItem= session.query(Category).filter_by(name=Category.name).one()
    if request.method =='POST':
	    if request.form['name']:
		    editedItem.name = request.form['name']
	   # NameOfItem = request.form['name']
	    if request.form['description']:
		    editedItem.description = request.form['description']
		if request.form['itemCategory']:
		    editedItem.itemCategory = session.query(Category).filter_by(name=request.form['category']).one()
        if request.form['image']:
		    editedItem.image = request.form['image']	
		session.add(editedItem)
	session.commit()
            flash("Successfully Edited!!!")
    return redirect(url_for('categories_view', catalog_id = categoryItem.category_id ,item_id = categoryItem.id))
	else:
		return render_template('edit.html', categories = categories, categoryItem = categoryItem)

		
  ### 3rd DELETE ITEMS
@app.route('/catalog/<int:catalog_id>/items/<int:item_id>/delete', methods=['GET', 'POST'])
@login_required
def deleteItem(categor_id, item_id):
    categoryItem = session.query(CategoryItem).filter_by(id = item_id).first()
	creator = getUserInfo(categoryItem.user_id)

	if creator.id != login_session['user_id']:
		return redirect('/login')

	if request.method == 'POST':
		session.delete(categoryItem)
		session.commit()
		return redirect(url_for('categories_view', catalog_id = categoryItem.category_id))
        
    else:
        return render_template('deleteItem.html', newData=newData)
		
@app.route('/login')
def login():
    log = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
	login_session['log'] =  log
	return render_template('login.html', LOG=log)

@app.route('/logout')
def logout():
    if login_session['provider'] == 'google':
        gdisconnected()
    del login_session['gplus_id']
    del login_session['access_token']

    del login_session['username']
    del login_session['email']	
	del login_session['image']
	del login_session['user_id']
	del login_session['provider']
	
	return redirect(url_for('showCategories'))
	
@app.route('/gconnect', methods=['POST'])
def gconnect():
	if request.args.get('log') != login_session['log']:
		response = make_response(json.dumps('Invalid log parameter.'), 401)
		response.headers['Content-Type'] = 'item/json'
		return response

	# Obtain authorization res
res = request.data
	try:
		oauth_flow = flow_from_clientsecrets('secretsClient.json', scope='')
		oauth_flow.redirect_uri = 'postmessage'
		credentials = oauth_flow.step2_exchange(res)
	except FlowExchangeError:
		response = make_response(json.dumps('Failed to upgrade the authorization res.'), 401)
		response.headers['Content-Type'] = 'item/json'
		return response

	access_token = credentials.access_token
	url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
	h = httplib2.Http()
	result = json.loads(h.request(url, 'GET')[1])

	if result.get('error') is not None:
		response = make_response(json.dumps(result.get('error')), 500)
		response.headers['Content-Type'] = 'item/json'
		return response

	gplus_id = credentials.id_token['sub']
	if result['user_id'] != gplus_id:
		response = make_response(json.dumps("Token's user ID doesn't match given user ID."), 401)
		response.headers['Content-Type'] = 'item/json'
		return response

	if result['issued_to'] != CLIENT_ID:
		response = make_response(json.dumps("Token's client ID does not match app's."), 401)
		print "Token's client ID does not match app's."
		response.headers['Content-Type'] = 'item/json'
		return response

	stored_access_token = login_session.get('access_token')
	stored_gplus_id = login_session.get('gplus_id')

	if stored_access_token is not None and gplus_id == stored_gplus_id:
		response = make_response(json.dumps('Current user is already connected.'), 200)
		response.headers['Content-Type'] = 'item/json'
		return response

	login_session['access_token'] = credentials.access_token
	login_session['gplus_id'] = gplus_id

	userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
	son = {'access_token': credentials.access_token, 'alt': 'json'}
	answer = requests.get(userinfo_url, son=son)

	data = answer.json()

	login_session['username'] = data['name']
	login_session['image'] = data['image']
	login_session['email'] = data['email']
	login_session['provider'] = 'google'

	user_id = getUserID(data["email"])
	if not user_id:
	    user_id = createUser(login_session)
	login_session['user_id'] = user_id

	return "Login Successful"

@app.route('/gdisconnect')
def gdisconnect():
	access_token = login_session.get('access_token')

	if access_token is None:
		response = make_response(json.dumps('Current user not connected.'), 401)
		response.headers['Content-Type'] = 'item/json'
		return response

	url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
	h = httplib2.Http()
	result = h.request(url, 'GET')[0]

	if result['status'] != '200':
	    response = make_response(json.dumps('Failed to revoke token for given user.'), 400)
	    response.headers['Content-Type'] = 'item/json'
	    return response

@app.route('/catalog/JSON')
def showJSONCategory():
	categories = session.query(Category).all()
	return jsonify(categories = [category.serialize for category in categories])

@app.route('/catalog/<int:catalog_id>/JSON')
@app.route('/catalog/<int:catalog_id>/items/JSON')
def showJSONCategory(catalog_id):
	categoryItems = session.query(CategoryItem).filter_by(category_id = catalog_id).all()
	return jsonify(categoryItems = [categoryItem.serialize for categoryItem in categoryItems])

@app.route('/catalog/<int:catalog_id>/items/<int:item_id>/JSON')
def showJSONCategoryItemJSON(catalog_id, item_id):
	categoryItem = session.query(CategoryItem).filter_by(id = item_id).first()
	return jsonify(categoryItem = [categoryItem.serialize])

if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)	
	

    
