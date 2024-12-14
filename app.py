from flask import Flask, request, render_template, jsonify
import db as Client
from bson import json_util


app = Flask(__name__)
db = Client.client.get_database('recipes')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/hello', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello, World!'})


@app.route('/ping', methods=['GET'])
def ping():
    response = Client.ping()
    return jsonify({'message': response})


@app.route('/recipes', methods=['GET'])
def get_recipes():
    response = db.recipes.find()
    return json_util.dumps(response)

@app.route('/recipes/find', methods=['GET'])
def find_recipes():
    ingredients = request.args.get('ingredients').split(',')
    ingredients = [{'$regex': ingredient, '$options': 'i'} for ingredient in ingredients]
    query = {'ingridients': {'$all': ingredients}}
    response = db.recipes.find(query)
    result = []
    for recipe in response:
        result.append(recipe)
    return json_util.dumps(result)


if __name__ == '__main__':
    app.run(port=5000)
