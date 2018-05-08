from flask import jsonify, request
from flask_pymongo import PyMongo
from random import randrange as rand
from flask import Flask

# from models.category import Category
# from models.comparison import Comparison
# from models.item import Item
# from models.topic import Topic

app = Flask(__name__)

@app.route('/')
def hello():
    return jsonify({'message': 'Welcome to CompRank!'})

categories = [
    {
        'id': 1,
        'name': "TUXC",
        'topics': ['Most Moral', 'Wettest']
    },
    {
        'id': 2,
        'name': 'Food & Drink',
        'topics': ['Sodas']
    }
]

comparisons = [
    {
        'id': 1,
        'item_a_id': 1,
        'item_b_id': 2,
        'winner_id': 1,
        'comparison_key': 'bdb3b5ba-0935-2177-83aa-0235c1a1826d'
    }
]

items = [
    {
        'id': 1,
        'name': 'Fanta',
        'description': '',
        'format': 'image',
        'image_link': '',
        'topic_id': 2,
        'rating': 9
    },
    {
        'id': 2,
        'name': 'Sprite',
        'description': '',
        'format': 'image',
        'image_link': '',
        'topic_id': 2,
        'rating': 22
    }
]


def error(m, code):
    return (jsonify(message=str(m)), code)


@app.route('/categories', methods=['GET'])
def get_categories():
    return jsonify(categories)


@app.route('/comparison/submit', methods=['POST'])
def submit_comparison():
    """ Submits a comparison of two items
    Request params:
        * comparison_key: STRING
        * winner_id: STRING
        * item_a_id: STRING
        * item_b_id: STRING
    Error responses:
        * Reason: Missing comparison_key param
          Code: 403
          Message: missing_param_comparison_key
        * Reason: Missing winner_id param
          Code: 403
          Message: missing_param_winner_id
        * Reason: Missing item_a_id param
          Code: 403
          Message: missing_param_item_a_id
        * Reason: Missing item_b_id param
          Code: 403
          Message: missing_param_item_b_id

    """
    request_data = request.get_json()
    print(request_data)
    if 'comparison_key' not in request_data:
        return error('missing_param_comparison_key', 400)
    if 'winner_id' not in request_data:
        return error('missing_param_winner_id', 400)
    if 'item_a_id' not in request_data:
        return error('missing_param_item_a_id', 400)
    if 'item_b_id' not in request_data:
        return error('missing_param_item_b_id', 400)

    response = {'comparison': 'comp'}
    return (jsonify(response), 201)


@app.route('/comparison/next', methods=['GET'])
def next_comparison():
    """ Submits a comparison of two items
    Query params:
        * topic: STRING
    """
    item_a_id = rand(len(items))
    item_b_id = rand(len(items))
    while item_a_id == item_b_id:
        item_b_id = rand(len(items))

    response = {
        'item_a': items[item_a_id],
        'item_b': items[item_b_id],
        'comparison_id': 'comp_id',
        'comparison_key': 'comp_key'
    }
    return (jsonify(response), 200)


@app.route('/rankings', methods=['GET'])
def get_rankings():
    """ Gets the first 10 rankings for a given topic
    Query params:
        * topic: STRING
        * key: STRING
    Error responses:
        * Reason: Missing topic param
          Code: 403
          Message: missing_param_topic
        * Reason: Missing key param
          Code: 403
          Message: missing_param_key
    """
    params = request.args
    if 'topic' not in params:
        return error('missing_param_topic', 400)
    if 'key' not in params:
        return error('missing_param_key', 400)

    n_to_take = 9
    ranked_items = (sorted(items, key=lambda item: item['rating'], reverse=True))
    response = {"rankings": ranked_items[:n_to_take]}
    return (jsonify(response), 200)


if __name__ == '__main__':
    app.run(debug=True)
