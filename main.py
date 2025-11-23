from werkzeug.utils import secure_filename

import flask as fl
import hashlib
import os
import sqlite3

app = fl.Flask(__name__)
app.secret_key = 'random string'
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png', 'gif', 'webp'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/login", methods = ['POST', 'GET'])
def login():
	if fl.request.method == 'POST':
		email = fl.request.form['email']
		password = fl.request.form['password']
		if is_valid(email, password):
			fl.session['email'] = email
			return fl.redirect(fl.url_for('root'))
		else:
			error = 'Invalid UserId / Password'
			return fl.render_template('login.html', error=error)

@app.route("/loginForm")
def loginForm():
	if 'email' in fl.session:
		return fl.redirect(fl.url_for('root'))
	else:
		return fl.render_template('login.html', error='')

def getLoginDetails():
	with sqlite3.connect('database.db') as conn:
		cur = conn.cursor()
		if 'email' not in fl.session:
			loggedIn = False
			firstName = ''
			noOfItems = 0
		else:
			loggedIn = True
			cur.execute("SELECT userId, firstName FROM users WHERE email = ?", (fl.session['email'], ))
			userId, firstName = cur.fetchone()
			cur.execute("SELECT count(productId) FROM interestedin WHERE userId = ?", (userId, ))
			noOfItems = cur.fetchone()[0]
	conn.close()
	return (loggedIn, firstName, noOfItems)

@app.route("/")
def root():
	loggedIn, firstName, noOfItems = getLoginDetails()
	with sqlite3.connect('database.db') as conn:
		cur = conn.cursor()
		cur.execute('SELECT productId, name, price, description, image, stock FROM products')
		itemData = cur.fetchall()
	itemData = parse(itemData)   
	return fl.render_template('home.html', itemData=itemData, loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems)

def isSuperUser():
	return (
		'email' in fl.session and (fl.session['email'] == 'sk@learner.manipal.edu' or fl.session['email'] == 'gmp@learner.manipal.edu')
	)

@app.route("/add")
def admin():
	if not isSuperUser():
		return fl.redirect(fl.url_for('root'))
	
	return fl.render_template('add.html')

def processProductForm():
	return (
		fl.request.form['name'], 
		float(fl.request.form['price']),
		fl.request.form['description'],
		int(fl.request.form['stock']),
	)

@app.route("/addItem", methods=["GET", "POST"])
def addItem():
	if not isSuperUser():
		return fl.redirect(fl.url_for('root'))

	if fl.request.method == "POST":
		name, price, description, stock = processProductForm()
		image = fl.request.files['image']
		filename = ''
		if image and allowed_file(image.filename):
			filename = secure_filename(image.filename)
			image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		imagename = filename
		with sqlite3.connect('database.db') as conn:
			try:
				cur = conn.cursor()
				cur.execute('''INSERT INTO products (name, price, description, image, stock) VALUES (?, ?, ?, ?, ?)''', (name, price, description, imagename, stock,))
				conn.commit()
			except:
				conn.rollback()
		conn.close()
		return fl.redirect(fl.url_for('root'))

@app.route("/remove")
def remove():
	if not isSuperUser():
		return fl.redirect(fl.url_for('root'))
	
	with sqlite3.connect('database.db') as conn:
		cur = conn.cursor()
		cur.execute('SELECT productId, name, price, description, image, stock FROM products')
		data = cur.fetchall()
	conn.close()
	return fl.render_template('remove.html', records=data)

@app.route("/removeItem")
def removeItem():
	if not isSuperUser():
		return fl.redirect(fl.url_for('root'))
	
	productId = fl.request.args.get('productId')
	with sqlite3.connect('database.db') as conn:
		try:
			cur = conn.cursor()
			cur.execute('DELETE FROM products WHERE productID = ?', (productId, ))
			conn.commit()
		except:
			conn.rollback()
	conn.close()
	return fl.redirect(fl.url_for('root'))

@app.route("/search", methods=['GET', 'POST'])
def search():
	data = []
	if fl.request.method == 'POST':
		name = fl.request.form['searchQuery']
		with sqlite3.connect('database.db') as conn:
			curr = conn.cursor()
			whereClause = '%{}%'.format(name)
			orderByClause = 'name desc'
			#orderByClause = 'charindex({}, name, 1) ASC'.format(name)
			curr.execute('SELECT * FROM products WHERE name LIKE ? ORDER BY ?', (whereClause, orderByClause))
			data = curr.fetchall()
		conn.close()
	return fl.render_template('search.html', records=data)

@app.route("/checkout")
def checkout():
	with sqlite3.connect('database.db') as conn:
		cur = conn.cursor()
		cur.execute('SELECT productId, name, price, description, image, stock FROM products')
		data = cur.fetchall()
	conn.close()
	return fl.render_template('checkout.html', data=data)

@app.route("/account/profile")
def profileHome():
	if 'email' not in fl.session:
		return fl.redirect(fl.url_for('root'))
	loggedIn, firstName, noOfItems = getLoginDetails()
	return fl.render_template("profileHome.html", loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems)

@app.route("/account/profile/edit")
def editProfile():
	if 'email' not in fl.session:
		return fl.redirect(fl.url_for('root'))
	loggedIn, firstName, noOfItems = getLoginDetails()
	with sqlite3.connect('database.db') as conn:
		cur = conn.cursor()
		cur.execute("SELECT userId, email, firstName, lastName, address1, address2, zipcode, city, state, country, phone FROM users WHERE email = ?", (fl.session['email'], ))
		profileData = cur.fetchone()
	conn.close()
	return fl.render_template("editProfile.html", profileData=profileData, loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems)

@app.route("/account/profile/changePassword", methods=["GET", "POST"])
def changePassword():
	if 'email' not in fl.session:
		return fl.redirect(fl.url_for('loginForm'))
	if fl.request.method == "POST":
		oldPassword = fl.request.form['oldpassword']
		oldPassword = hashlib.md5(oldPassword.encode()).hexdigest()
		newPassword = fl.request.form['newpassword']
		newPassword = hashlib.md5(newPassword.encode()).hexdigest()
		with sqlite3.connect('database.db') as conn:
			cur = conn.cursor()
			cur.execute("SELECT userId, password FROM users WHERE email = ?", (fl.session['email'], ))
			userId, password = cur.fetchone()
			if (password == oldPassword):
				try:
					cur.execute("UPDATE users SET password = ? WHERE userId = ?", (newPassword, userId))
					conn.commit()
					msg="Changed successfully"
				except:
					conn.rollback()
					msg = "Failed"
				return fl.render_template("changePassword.html", msg=msg)
			else:
				msg = "Wrong password"
		conn.close()
		return fl.render_template("changePassword.html", msg=msg)
	else:
		return fl.render_template("changePassword.html")
	
def processUserForm():
	return (
		fl.request.form['email'],
		fl.request.form['password'],
		fl.request.form['firstName'],
		fl.request.form['lastName'],
		fl.request.form['address1'],
		fl.request.form['address2'],
		fl.request.form['zipcode'],
		fl.request.form['city'],
		fl.request.form['state'],
		fl.request.form['country'],
		fl.request.form['phone'],
	)

@app.route("/updateProfile", methods=["GET", "POST"])
def updateProfile():
	if fl.request.method == 'POST':
		email, _, firstName, lastName, address1, address2, zipcode, city, state, country, phone = processUserForm()
		with sqlite3.connect('database.db') as con:
				try:
					cur = con.cursor()
					cur.execute('UPDATE users SET firstName = ?, lastName = ?, address1 = ?, address2 = ?, zipcode = ?, city = ?, state = ?, country = ?, phone = ? WHERE email = ?', (firstName, lastName, address1, address2, zipcode, city, state, country, phone, email))
					con.commit()
				except:
					con.rollback()
		con.close()
		return fl.redirect(fl.url_for('editProfile'))


@app.route("/productDescription")
def productDescription():
	loggedIn, firstName, noOfItems = getLoginDetails()
	productId = fl.request.args.get('productId')
	with sqlite3.connect('database.db') as conn:
		cur = conn.cursor()
		cur.execute('SELECT productId, name, price, description, image, stock FROM products WHERE productId = ?', (productId, ))
		productData = cur.fetchone()
	conn.close()
	return fl.render_template("productDescription.html", data=productData, loggedIn = loggedIn, firstName = firstName, noOfItems = noOfItems)

@app.route("/addToCart")
def addToCart():
	if 'email' not in fl.session:
		return fl.redirect(fl.url_for('loginForm'))
	else:
		productId = int(fl.request.args.get('productId'))
		with sqlite3.connect('database.db') as conn:
			cur = conn.cursor()
			cur.execute("SELECT userId FROM users WHERE email = ?", (fl.session['email'], ))
			userId = cur.fetchone()[0]
			try:
				cur.execute("INSERT INTO interestedin (userId, productId) VALUES (?, ?)", (userId, productId))
				conn.commit()
			except:
				conn.rollback()
		conn.close()
		return fl.redirect(fl.url_for('root'))

@app.route("/cart")
def cart():
	if 'email' not in fl.session:
		return fl.redirect(fl.url_for('loginForm'))
	loggedIn, firstName, noOfItems = getLoginDetails()
	email = fl.session['email']
	with sqlite3.connect('database.db') as conn:
		cur = conn.cursor()
		cur.execute("SELECT userId FROM users WHERE email = ?", (email, ))
		userId = cur.fetchone()[0]
		cur.execute("SELECT products.productId, products.name, products.price, products.image FROM products, interestedin WHERE products.productId = interestedin.productId AND interestedin.userId = ?", (userId, ))
		products = cur.fetchall()
	totalPrice = 0
	for row in products:
		totalPrice += row[2]
	return fl.render_template("cart.html", products = products, totalPrice=totalPrice, loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems)

@app.route("/removeFromCart")
def removeFromCart():
	if 'email' not in fl.session:
		return fl.redirect(fl.url_for('loginForm'))
	email = fl.session['email']
	productId = int(fl.request.args.get('productId'))
	with sqlite3.connect('database.db') as conn:
		cur = conn.cursor()
		cur.execute("SELECT userId FROM users WHERE email = ?", (email, ))
		userId = cur.fetchone()[0]
		try:
			cur.execute("DELETE FROM interestedin WHERE userId = ? AND productId = ?", (userId, productId))
			conn.commit()
		except:
			conn.rollback()
	conn.close()
	return fl.redirect(fl.url_for('root'))

@app.route("/logout")
def logout():
	fl.session.pop('email', None)
	return fl.redirect(fl.url_for('root'))

def is_valid(email, password):
	con = sqlite3.connect('database.db')
	cur = con.cursor()
	cur.execute('SELECT email, password FROM users')
	data = cur.fetchall()
	for row in data:
		if row[0] == email and row[1] == hashlib.md5(password.encode()).hexdigest():
			return True
	return False

@app.route("/register", methods = ['GET', 'POST'])
def register():
	if fl.request.method == 'POST':
		#Parse form data    
		email, password, firstName, lastName, address1, address2, zipcode, city, state, country, phone = processUserForm()

		with sqlite3.connect('database.db') as con:
			try:
				cur = con.cursor()
				cur.execute('INSERT INTO users (password, email, firstName, lastName, address1, address2, zipcode, city, state, country, phone) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (hashlib.md5(password.encode()).hexdigest(), email, firstName, lastName, address1, address2, zipcode, city, state, country, phone))

				con.commit()

				msg = "Registered Successfully"
			except:
				con.rollback()
				msg = "Error occured"
		con.close()
		return fl.render_template("login.html", error=msg)

@app.route("/registerationForm")
def registrationForm():
	return fl.render_template("register.html")

def allowed_file(filename):
	return '.' in filename and \
			filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def parse(data):
	ans = []
	i = 0
	while i < len(data):
		curr = []
		for _ in range(6):
			if i >= len(data):
				break
			curr.append(data[i])
			i += 1
		ans.append(curr)
	return ans

if __name__ == '__main__':
	app.run(debug=True)
