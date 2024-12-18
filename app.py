from flask import Flask, request, render_template, jsonify, Response
from bson import json_util

import db as mongoDb

app = Flask(__name__)
db = mongoDb.client.get_database('recipes')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/hello', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello, World!'})


@app.route('/ping', methods=['GET'])
def ping():
    response = mongoDb.ping()
    return jsonify({'message': response})


@app.route('/recipes', methods=['GET'])
def get_recipes():
    response = db.recipes.aggregate([{'$sample': {'size': 1}}])
    recipe = next(response, None)
    return Response(json_util.dumps(recipe, indent=4), content_type='application/json')


@app.route('/recipes/find', methods=['GET'])
def find_recipes():
    ingredients = request.args.get('ingredients')

    if ingredients:
        ingredients = ingredients.split(',')
        pipeline = [
            {
                '$match': {
                    '$and': [
                        {'ingridients': {'$regex': ingredient, '$options': 'i'}} for ingredient in ingredients
                    ]
                }
            },
            {
                '$addFields': {
                    'calories_int': {'$toInt': '$nutritions.calories'},
                    'ingredients_count': {'$size': '$ingridients'}
                }
            },
            {
                '$sort': {
                    'ingredients_count': 1,
                    'calories_int': -1
                }
            }, {
                '$project': {
                    '_id': 0,
                    'title': '$basic_info.title',
                    'prep_data': 1,
                    'ingridients': 1,
                    'nutritions': 1
                }
            }
        ]

        response = db.recipes.aggregate(pipeline)
        result = [recipe for recipe in response]

        return Response(json_util.dumps(result), content_type='application/json')
    return render_template('find.html')


if __name__ == '__main__':
    app.run(port=5000)
