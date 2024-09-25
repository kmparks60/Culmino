import os
from flask import Flask
from markupsafe import Markup
from dotenv import load_dotenv
from flask_pymongo import PyMongo

load_dotenv()
mongo_secret_key = os.getenv("SECRET_KEY")
mongo_uri = os.getenv("MONGO_URI")

app = Flask(__name__)
app.config["SECRET_KEY"] = mongo_secret_key
app.config["MONGO_URI"] = mongo_uri

# Setup MongoDB
mongodb_client = PyMongo(app)
db = mongodb_client.cx["pymongo_tutorial"]

@app.template_filter('nl2br')
def nl2br(value):
	return Markup(value.replace("\n", '<br>'))

#Testing
# print(f"mongodb_client: {mongodb_client}")
# print(f"db: {db}")

from application import routes