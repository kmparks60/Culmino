from application import app
from flask import render_template, request, redirect, flash
from datetime import datetime
from .forms import TodoForm
from bson import ObjectId
from application import db
from datetime import datetime

@app.route("/")
def get_todos():
	todos = []
	form = TodoForm()
	for todo in db.todos.find().sort("date_created", -1):
		todo["_id"] = str(todo["_id"])
		todo["date_created"] = todo["date_created"].strftime("%b %d %Y %H:%M:%S")
		todos.append(todo)
	return render_template("view_todos.html", title="Layout Page", todos=todos, form=form)

@app.route("/add_todo", methods = ['POST', 'GET'])
def add_todo():
	form = TodoForm(request.form)
	if form.validate_on_submit():
		todo_name = form.name.data
		todo_description = form.description.data
		completed = form.completed.data

		db.todos.insert_one({
			"name": todo_name,
			"description": todo_description,
			"completed": completed,
			"date_created": datetime.now()
		})
		flash("Note successfully added", "success")
	else:
		flash("Failed to add note. Please check the form.", "danger")
	return redirect("/")

@app.route("/update_todo/<id>", methods = ["POST", "GET"])
def update_todo(id):
	if request.method == "POST":
		form = TodoForm(request.form)
		todo_name = form.name.data
		todo_description = form.description.data
		completed = form.completed.data

		db.todos.find_one_and_update({"_id": ObjectId(id)}, {"$set": {
			"name": todo_name,
			"description": todo_description,
			"completed": completed,
			"date_created": datetime.now()
		}})

		flash("Note successfully updated", "success")
		return redirect("/")
	
	else:
		form = TodoForm()

		todo = db.todos.find_one_or_404({"_id": ObjectId(id)})
		form.name.data = todo.get("name", None)
		form.description.data = todo.get("description", None)
		form.completed.data = todo.get("completed", None)

	return render_template("update_todos.html", form = form, todo_id=id)

@app.route("/delete_todo/<id>")
def delete_todo(id):
	db.todos.find_one_and_delete({"_id": ObjectId(id)})
	flash("Note successfully deleted", "success")
	return redirect("/")