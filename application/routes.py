from application import app
from flask import render_template, request, redirect, flash, session
from .forms import TodoForm, SignupForm, LoginForm
from bson import ObjectId
from application import db
from datetime import datetime
from .models import User

@app.route("/")
def get_todos():
	todos = []
	form = TodoForm()
	
	if 'username' in session:
		todos = db.todos.find({
			"$or": [
				{"creator": session['username']},
				{"shared_with": session['username']}
			]
		}).sort("date_created", -1)
	else:
		todos = db.todos.find({"name": "Sample Note"}).sort("date_created", -1)

	todo_list = []
	for todo in todos:
		todo["_id"] = str(todo["_id"])
		todo["date_created"] = todo["date_created"].strftime("%b %d %Y %H:%M:%S")
		todo_list.append(todo)
	return render_template("view_todos.html", title="Layout Page", todos=todo_list, form=form)

@app.route("/add_todo", methods = ['POST', 'GET'])
def add_todo():
	form = TodoForm(request.form)
	if form.validate_on_submit():
		todo_name = form.name.data
		todo_description = form.description.data
		completed = form.completed.data
		share_with = [user.strip() for user in form.share_with.data.split(',')]

		db.todos.insert_one({
			"name": todo_name,
			"description": todo_description,
			"completed": completed,
			"shared_with": share_with,
			"date_created": datetime.now(),
			"creator": session.get('username')
		})
		flash("Note successfully added", "success")
	else:
		flash("Failed to add note. Please check the form.", "danger")
	return redirect("/")

@app.route("/update_todo/<id>", methods = ['POST', 'GET'])
def update_todo(id):
	if request.method == "POST":
		form = TodoForm(request.form)
		todo_name = form.name.data
		todo_description = form.description.data
		completed = form.completed.data
		share_with = [user.strip() for user in form.share_with.data.split(',')]

		db.todos.find_one_and_update({"_id": ObjectId(id)}, {"$set": {
			"name": todo_name,
			"description": todo_description,
			"completed": completed,
			"shared_with": share_with,
			"date_created": datetime.now()
		}})

		flash("Note successfully updated", "success")
		return redirect("/")
	
	else:
		form = TodoForm()

		todo = db.todos.find_one_or_404({"_id": ObjectId(id)})
		form.name.data = todo.get("name", None)
		form.description.data = todo.get("description", None)
		form.completed.data = todo.get("completed", False)
		form.share_with.data = ','.join(todo.get("shared_with", []))

	return render_template("update_todos.html", form = form, todo_id=id)

@app.route("/delete_todo/<id>")
def delete_todo(id):
	db.todos.find_one_and_delete({"_id": ObjectId(id)})
	return redirect("/")

@app.route("/signup", methods = ['POST', 'GET'])
def signup():
	form = SignupForm()
	error_message = None

	if form.validate_on_submit():
		username = form.username.data
		email = form.email.data
		password = form.password.data

		if User.find_by_username(username):
			error_message = "User already exists! Please choose a different username."
		else:
			new_user = User(username=username, email=email, password=password)
			new_user.save()
			return redirect("/login")

	return render_template('signup.html', form=form, error_message=error_message)

@app.route("/login", methods = ['GET', 'POST'])
def login():
	form = LoginForm(request.form)
	if request.method == 'POST':
		username = form.username.data
		password = form.password.data

		if User.validate_password(username, password):
			session['username'] = username
			flash("Logged in successfully.", "success")
			return redirect("/")
		else:
			flash("Invalid username or password.", "danger")
	return render_template("login.html", form=form)

@app.route("/logout")
def logout():
	session.pop('username', None)
	flash("Logged outsuccessfully.", "success")
	return redirect("/")