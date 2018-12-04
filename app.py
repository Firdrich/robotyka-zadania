from flask import Flask, session, redirect, url_for, request, render_template, flash
from database import DataBase
from profile import Profile
from flask_session import Session
import sys
import time

#configuring stuff
app = Flask(__name__)
app.secret_key = "jdu7x3j8e83iej7eeh8e"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
	db = DataBase()
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		if db.login_to_account(username,password):
			session['logged_in'] = True
			session['username'] = request.form['username']
			print(db.get_user_admin(username))
			if db.get_user_admin(username) == 1:
				session['admin'] = True
			else:
				session['admin'] = False
			return render_template('index.html')
		else:
			session['logged_in'] = False
			flash("You typed wrong username or password!")
			return render_template('login.html')
	else:
		return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
	db = DataBase()
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']
		if db.add_account(username,password,email):
			flash("You were successfully registered!")
			return render_template('register.html')
		else:
			flash("That user arleady exist")
			return render_template('register.html')
	return render_template('register.html')


@app.route('/logout',methods=['GET'])
def logut():
	#session['logged_in'] = False
	session.clear()
	return redirect(url_for('index'))

@app.route('/settings',methods=['GET','POST'])
def settings():
	username = session['username']
	db = DataBase()
	profile = Profile(db.get_user_id(username))
	if request.method == 'POST':
		username = session['username']
		if 'ProfileData' in request.form:
			name = request.form.get('name')
			surname = request.form.get('surname')
			age = request.form.get('age')
			sex = request.form.get('sex')
			if name != "":
				db.change_setting("name",name,username)
			if surname != "":
				db.change_setting("surname",surname,username)
			if age != "":
				db.change_setting("age",age,username)
			if sex != "":
				db.change_setting("sex",sex,username)
				flash("Successfully changed informations")
		if 'ChangeMail' in request.form:
			newmail = request.form['email']
			db.change_email(newmail,username)
			flash("Successfully changed mail")
		if 'ChangePassword' in request.form:
			password = request.form['password']
			newpassword = request.form['newpassword']
			repeatpassword = request.form['repeatpassword']
			if db.get_user_password(username) == password:
				if newpassword == repeatpassword:
					db.change_password(newpassword,username)
					flash("Successfully changed password")
				else:
					flash("Passwords are not the same")
			else:
				print(db.get_user_password(username))
				print(password)
				flash("You typed wrong password")
		return redirect(url_for('settings'))

	return render_template('settings.html', profile = profile)

@app.route('/admin/<id>', methods=['POST'])
def del_post(id):
	try:
		if session['admin'] == True:
			db = DataBase()
			db.delete_exercise(id)
			return redirect(url_for('admin'))
	except KeyError:
		return render_template('notlogin.html')

@app.route('/admin', methods=['GET','POST'])
def admin():
	try:
		if session['admin'] == True:
			db = DataBase()
			if request.method == 'POST': 	#if new exercise is added through form
				exercise_header = request.form.get('header')
				exercise_content = request.form.get('content')
				exercise_time = request.form.get('time')
				db.add_exercise(exercise_time, exercise_content, exercise_header) #adds new exercise according to form
			times = db.get_exercise_time()
			content = db.get_exercise_content()
			titles = db.get_exercise_titles()
			id = db.get_exercise_id()
			print(session['admin'])
			return render_template('admin.html',times=times, content=content, titles=titles, id=id)
	except KeyError:
		return render_template('notlogin.html')

@app.route('/exercises', methods=['GET','POST'])
def exercises(): #Simply displays exercises
	db = DataBase()
	content = db.get_exercise_content()
	titles = db.get_exercise_titles()
	id = db.get_exercise_id()
	return render_template('exercises.html', titles=titles, content=content, id=id)

@app.route('/exercises/<id>', methods=['POST']) #Beggining exercise through start_exercise() in database.py
def begin_exercise(id):
	db = DataBase()
	user = db.get_user_id(session['username'])
	exercise = db.get_exercise(id) #gets list of one exercise entries by id
	exercise_id = exercise[0]
	exercise_time = exercise[1] * 3600 #takes time from database and converts to hours
	date = int(time.time()) #takes systemtime
	db.start_exercise(user, exercise_id, exercise_time, date)
	return redirect(url_for('exercises'))

@app.route('/exercises/answers/<id>', methods=['POST']) #Display an answer to exercise
def answers(id):
	#WARNING DATABASE NOT UPDATED TO SUPPORT THIS!!!
	work_in_progress = True
	if work_in_progress == True:
		return "Work in Progress"
	db = Database()
	user = db.get_user_id(session['username'])
	exercise_time = get_time_till_answer(user, id) #gets time to unlock exercise
	if exercise_time < int(time.time()): #if current system time is bigger than time from database
		answer = get_exercise_answer(id)
		return render_template('exercise.html', answer=answer) #return template with answer to exercise
	else:
		return render_template('notyet.html') #else return template without an answer




if __name__ == '__main__':
	app.secret_key = "jdu7x3j8e83iej7eeh8e"
	app.run(port=5011)
