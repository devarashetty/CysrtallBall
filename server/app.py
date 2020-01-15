'''server/app.py - main api app declaration'''
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from flask_pymongo import PyMongo
from server.models.users import getUsersList

'''Main wrapper for app creation'''
app = Flask(__name__, static_folder='../build')
app.config["MONGO_URI"] = "mongodb://localhost:27017/crystalballDemo"
mongo = PyMongo(app)

CORS(app)

##
# API routes
##

@app.route('/api/items')
def items():
  '''Sample API route for data'''
  return jsonify([{'title': 'A'}, {'title': 'B'}])

@app.route('/api/usersList')
def usersList():
  return getUsersList(mongo)
  # return jsonify([{'title': 'A'}, {'title': 'B'}])

##
# View route
##

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
  '''Return index.html for all non-api routes'''
  #pylint: disable=unused-argument
  return 'Route Not Found'