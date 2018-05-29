from flask import Flask
# from flask_pymongo import PyMongo
from pymongo import MongoClient
import json

app = Flask(__name__)

client = MongoClient('mongodb://botnlu:toanloc96#_@ds016298.mlab.com:16298/botnlu')

# app.config['MONGO_DBNAME'] = 'botnlu'
# app.config['MONGO_URI'] = 'mongodb://botnlu:toanloc96#_@ds016298.mlab.com:16298/botnlu'

# mongo = PyMongo(app)

@app.route('/add')
def add():
    # user = mongo.db.users
    # user.insert({'name' : 'Anthony', 'abl': ["luc", 'last']})
    # return 'Add user!'
    db = client.botnlu
    collection = db['users']
    r = collection.find_one()
    return "dgfdg"

if __name__== '__main__':
    app.run(debug=True)