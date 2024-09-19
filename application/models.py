from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash

from application import db

class User:
	def __init__(self, username, email, password):
		self.username = username
		self.email = email
		self.password = generate_password_hash(password)

	def save(self):
		db.users.insert_one({
			'username': self.username,
			'email': self.email,
			'password': self.password
		})

	@staticmethod
	def find_by_username(username):
		return db.users.find_one({'username': username})
	
	@staticmethod
	def validate_password(username, password):
		user = User.find_by_username(username)
		if user:
			return check_password_hash(user['password'], password)
		return False