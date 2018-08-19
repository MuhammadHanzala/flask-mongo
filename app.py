from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'MONGO_DBNAME'
app.config['MONGO_URI'] = 'MONGO_URI'

mongo = PyMongo(app)

@app.route('/todo', methods=['POST'])
def add_todo():
  db = mongo.db.todo
  title = request.json['title']
  status = request.json['status']
  todo_id = db.insert({'title': title, 'status': status})
  new_todo = db.find_one({'_id': todo_id })
  output = {'title' : new_todo['title'], 'status' : new_todo['status'], '_id': str(new_todo['_id'])}
  return jsonify({'result' : output})

@app.route('/todos', methods=['GET'])
def get_todos():
  todos = mongo.db.todo.find()
  output = []
  for todo in todos:
    output.append({'title' : todo['title'], 'status' : todo['status'], '_id': str(todo['_id'])})
  return jsonify({'result' : output})

@app.route('/todo/<title>', methods=['GET'])
def get_todo(title):
  todos = mongo.db.todo.find({'title': title})
  output = []
  for todo in todos:
    output.append({'title' : todo['title'], 'status' : todo['status'], '_id': str(todo['_id'])})
  return jsonify({'result' : output})

@app.route('/todo/<_id>', methods=['DELETE'])
def delete_todo(_id):
  db = mongo.db.todo
  db.delete_one({'_id': ObjectId(_id)})
  output = []
  for todo in todo.find():
    output.append({'title' : todo['title'], 'status' : todo['status'], '_id': str(todo['_id'])})
  return jsonify({'result' : output})

@app.route('/todo/<_id>', methods=['PUT'])
def edit_todo(_id):
  db = mongo.db.todo
  todo = db.find_one({'_id': ObjectId(_id)})
  todo['title'] = request.json['title']
  todo['status'] = request.json['status']
  db.save(todo)
  output = {'title' : todo['title'], 'status' : todo['status'], '_id': str(todo['_id'])}
  return jsonify({'result' : output})

