import os
from flask import Flask
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

#Testing
# print(f"mongodb_client: {mongodb_client}")
# print(f"db: {db}")

from application import routes