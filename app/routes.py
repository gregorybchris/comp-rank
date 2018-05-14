from flask import jsonify, request
from app import app
from random import randrange
import json
import uuid
import os
from models.category import Category
from models.topic import Topic
from models.comparison import Comparison
from models.item import Item
from mongoengine import DoesNotExist


def error(m, code):
    return (jsonify(message=str(m)), code)


@app.route('/')
def hello():
    return jsonify({'message': 'Welcome to CompRank!'})


@app.route('/categories', methods=['GET'])
def get_categories():
    """ Gets a list of all categories """
    categories = Category.objects()
    serialized_categories = [c.serialize() for c in categories if c.enabled]
    response = {'categories': serialized_categories}
    return (jsonify(response), 200)


@app.route('/comparison/next', methods=['GET'])
def next_comparison():
    """ Returns a comparison of two items
    Query params:
        * topic_id: STRING
    Error responses:
        * Reason: Missing topic id param
          Code: 403
          Message: missing_param_topic_id
        * Reason: Invalid topic id param
          Code: 403
          Message: invalid_param_topic_id
        * Reason: Not enough items to compare
          Code: 500
          Message: insufficient_records
    """

    params = request.args
    if 'topic_id' not in params:
        return error('missing_param_topic_id', 400)
    topic_id = params['topic_id']

    try:
        topic = Topic.objects.get(id=topic_id)
    except DoesNotExist:
         return error('invalid_param_topic_id', 403)

    num_items = len(topic.items)
    print(num_items)
    if num_items < 2:
        return error('insufficient_records', 500)

    item_a_index = randrange(num_items)
    item_b_index = item_a_index
    while item_b_index == item_a_index:
        item_b_index = randrange(num_items)

    item_a = topic.items[item_a_index]
    item_b = topic.items[item_b_index]
    comparison = Comparison(item_a=item_a, item_b=item_b)
    comparison.save()

    response = {'comparison': comparison.serialize()}
    # response = {'comparison': 'TODO'}
    return (jsonify(response), 200)


@app.route('/comparison/submit', methods=['POST'])
def submit_comparison():
    """ Submits a comparison of two items
    Request params:
        * key: STRING
        * past_keys: LIST<STRING>
        * winner_id: STRING
    Error responses:
        * Reason: Missing key param
          Code: 403
          Message: missing_param_key
        * Reason: Missing winner_id param
          Code: 403
          Message: missing_param_winner_id
        * Reason: Invalid key param
          Code: 400
          Message: invalid_param_key
        * Reason: Invalid winner_id param
          Code: 400
          Message: invalid_param_winner_id
        * Reason: Comparison key already used
          Code: 400
          Message: comparison_already_completed
        * Reason: One past key was for an incomplete comparison
          Code: 400
          Message: past_key_not_completed
        * Reason: One past key was invalid
          Code: 403
          Message: invalid_param_past_keys
    """
    COMPARISONS_NEEDED = 5

    request_data = request.get_json()
    if 'key' not in request_data:
        return error('missing_param_key', 403)
    key = request_data['key']
    if 'winner_id' not in request_data:
        return error('missing_param_winner_id', 403)
    winner_id = request_data['winner_id']
    if 'past_keys' in request_data:
        past_keys = request_data['past_keys']
        for past_key in request_data['past_keys']:
            try:
                comparison = Comparison.objects.get(key=past_key)
                if not comparison.winning_item:
                    return error('past_key_not_completed', 400)
            except DoesNotExist:
                return error('invalid_param_past_keys', 403)

    try:
        comparison = Comparison.objects.get(key=key)
    except DoesNotExist:
        return error('invalid_param_key', 400)

    if comparison.winning_item:
        return error('comparison_already_completed', 400)

    try:
        winning_item = Item.objects.get(id=winner_id)
    except DoesNotExist:
        return error('invalid_param_winner_id', 400)

    comparison.winning_item = winning_item
    comparison.save()

    if 'past_keys' in request_data and len(past_keys) + 1 >= COMPARISONS_NEEDED:
        response = {
            'unlocked': 'True',
            'topic_key': str(uuid.UUID(bytes=os.urandom(16)))
        }
    else:
        response = {'unlocked': 'False'}


    return (jsonify(response), 201)


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
        return error('missing_param_topic', 403)
    topic = params['topic']
    if 'topic_key' not in params:
        return error('missing_param_topic_key', 403)
    topic_key = params['topic_key']

    # n_to_take = 10
    # top_items = mongo.db.item.find().sort('rating', DESCENDING).limit(n_to_take)
    # top_items_serialized = list(map(serialize, top_items))
    response = {'rankings': 'TODO'}
    return (jsonify(response), 200)
