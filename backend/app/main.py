from flask import jsonify, request, Flask
from random import randrange
import json
import uuid
import os
from .category import Category
from .topic import Topic
from .comparison import Comparison
from .item import Item
from mongoengine import DoesNotExist, connect
from flask_cors import CORS, cross_origin


app = Flask(__name__)
# TODO: Maybe I don't need this?
app.config['MONGODB_SETTINGS'] = {
    'db': 'comprank',
    'host': os.environ.get('MONGODB_URI', None)
}

CORS(app)
connect('comprank', host=os.environ.get('MONGODB_URI', None))


def error(m, code):
    """Get error message."""
    return (jsonify(message=str(m)), code)


@app.route('/')
def hello():
    """Hello message."""
    return jsonify({
        'message': 'Welcome to CompRank!',
        'version': '1.0.2'
    })


@app.route('/categories', methods=['GET'])
def get_categories():
    """Get a list of all categories."""
    categories = Category.objects()
    serialized_categories = [c.serialize() for c in categories if c.enabled]
    response = {'categories': serialized_categories}
    return (jsonify(response), 200)


@app.route('/topic', methods=['GET'])
def get_topic():
    """
    Get information on a topic.

    Query params:
        * topic_id: STRING
    Error responses:
        * Reason: Missing topic id param
          Code: 403
          Message: missing_param_topic_id
        * Reason: Invalid topic id param
          Code: 403
          Message: invalid_param_topic_id
        * Reason: Expired topic
          Code: 403
          Message: topic_expired
    """
    params = request.args
    if 'topic_id' not in params:
        return error('missing_param_topic_id', 400)
    topic_id = params['topic_id']

    try:
        topic = Topic.objects.get(id=topic_id)
    except DoesNotExist:
        return error('invalid_param_topic_id', 403)

    if not topic.enabled:
        return error('topic_expired', 403)

    response = {'topic': topic.serialize()}
    return (jsonify(response), 200)


@app.route('/comparison/next', methods=['GET'])
def next_comparison():
    """
    Return a comparison of two items.

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
          Code: 400
          Message: no_items_to_compare
    """
    params = request.args
    if 'topic_id' not in params:
        return error('missing_param_topic_id', 400)
    topic_id = params['topic_id']

    try:
        topic = Topic.objects.get(id=topic_id)
    except DoesNotExist:
        return error('invalid_param_topic_id', 403)

    enabled_items = list(filter(lambda item: item.enabled, topic.items))

    num_items = len(enabled_items)
    if num_items < 2:
        return error('no_items_to_compare', 400)

    item_a_index = randrange(num_items)
    item_b_index = item_a_index
    while item_b_index == item_a_index:
        item_b_index = randrange(num_items)

    item_a = enabled_items[item_a_index]
    item_b = enabled_items[item_b_index]
    comparison = Comparison(item_a=item_a, item_b=item_b, topic=topic,
                            address=request.remote_addr)
    comparison.save()

    response = {'comparison': comparison.serialize()}
    return (jsonify(response), 200)


@app.route('/comparison/submit', methods=['POST'])
def submit_comparison():
    """ Submits a comparison of two items
    Request params:
        * key: STRING
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
        * Reason: Invalid winner_id param, not an item
          Code: 400
          Message: winner_id_not_found
        * Reason: Invalid winner_id param, not in this comparison
          Code: 400
          Message: winner_not_in_comparison
        * Reason: Comparison key already used
          Code: 400
          Message: comparison_already_completed
    """
    request_data = request.get_json()
    if 'key' not in request_data:
        return error('missing_param_key', 403)
    key = request_data['key']
    if 'winner_id' not in request_data:
        return error('missing_param_winner_id', 403)
    winner_id = request_data['winner_id']

    try:
        comparison = Comparison.objects.get(key=key)
    except DoesNotExist:
        return error('invalid_param_key', 400)

    if comparison.winning_item:
        return error('comparison_already_completed', 400)

    try:
        winning_item = Item.objects.get(id=winner_id)
    except DoesNotExist:
        return error('winner_id_not_found', 400)

    if winner_id not in [str(comparison.item_a.id), str(comparison.item_b.id)]:
        return error('winner_not_in_comparison', 400)

    comparison.winning_item = winning_item
    comparison.save()
    winning_item.rating = winning_item.rating + 1
    winning_item.save()

    response = {
        'message': 'submitted'
    }
    return (jsonify(response), 201)


@app.route('/rankings', methods=['POST'])
def get_rankings():
    """ Gets the first 10 rankings for a given topic
    Query params:
        * topic_id: STRING
        * keys: LIST<STRING>
    Error responses:
        * Reason: Missing topic_id param
          Code: 403
          Message: missing_param_topic_id
        * Reason: Invalid topic
          Code: 403
          Message: invalid_topic_id
        * Reason: Missing keys param
          Code: 403
          Message: missing_param_keys
        * Reason: One comparison key was for an incomplete comparison
          Code: 400
          Message: comparison_key_not_completed
        * Reason: One comparison key was for a comparison for the wrong topic
          Code: 400
          Message: comparison_key_wrong_topic
        * Reason: One comparison key was invalid
          Code: 403
          Message: invalid_param_keys
    """
    COMPARISONS_NEEDED = 10
    NUM_ITEMS = 10

    request_data = request.get_json()
    if 'topic_id' not in request_data:
        return error('missing_param_topic_id', 403)
    topic_id = request_data['topic_id']
    if 'keys' not in request_data:
        return error('missing_param_keys', 403)
    keys = request_data['keys']

    try:
        topic = Topic.objects.get(id=topic_id)
    except DoesNotExist:
        return error('invalid_topic_id', 403)

    for key in keys:
        try:
            comparison = Comparison.objects.get(key=key)
            if not comparison.winning_item:
                return error('comparison_key_not_completed', 400)
            if str(comparison.topic.id) != topic_id:
                return error('comparison_key_wrong_topic', 400)
        except DoesNotExist:
            return error('invalid_param_keys', 403)

    unlocked = len(keys) >= COMPARISONS_NEEDED
    if not unlocked:
        return (jsonify({'unlocked': False}), 201)

    sorted_items = sorted(topic.items, key=lambda t: t.rating, reverse=True)
    items = sorted_items[:NUM_ITEMS]
    serialized_items = [item.serialize() for item in items if item.enabled]

    response = {
        'unlocked': True,
        'items': serialized_items
    }
    return (jsonify(response), 201)


if __name__ == '__main__':
    app.run(debug=True)
