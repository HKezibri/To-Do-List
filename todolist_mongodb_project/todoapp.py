from flask import Flask, render_template, request, url_for, redirect
from bson.objectid import ObjectId
import pymongo

app = Flask(__name__)

conn = pymongo.MongoClient("mongodb://localhost:27017/")

db = conn["ToDoListe"]["myliste"]

@app.route('/')
def home():
    saved_todos = db.find()
    return render_template('home.html', db=saved_todos)

@app.route('/add', methods=['POST'])
def add_todo():
    new_todo = request.form.get('new-todo')
    db.insert_one({'text' : new_todo, 'complete' : False})
    return redirect(url_for('home'))

@app.route('/complete/<oid>')
def complete(oid):
    todo_item = db.find_one({'_id': ObjectId(oid)})
    todo_item['complete'] = True
    db.save(todo_item)
    return redirect(url_for('home'))

@app.route('/delete_completed')
def delete_completed():
    db.delete_many({'complete' : True})
    return redirect(url_for('home'))

@app.route('/delete_all')
def delete_all():
    db.delete_many({})
    return redirect(url_for('home'))


if __name__=="__main__":
    app.run(debug=True)