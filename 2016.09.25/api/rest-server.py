#!flask/bin/python
from flask import Flask, jsonify, abort, url_for, request
from data.rooms import rooms

from data.objects import objects

app = Flask(__name__)


@app.route('/', methods=['GET'])
def get_structure():
    return jsonify({'rooms': url_for('get_rooms'), 'objects': url_for('get_objects')})


@app.route('/rooms/', methods=['GET'])
def get_rooms():
    print(request.headers)
    return jsonify({'rooms': rooms})


@app.route('/room_list/', methods=['GET'])
def get_rooms_list():
    print(request.headers)
    return jsonify(rooms)


@app.route('/rooms/<string:room_id>', methods=['GET'])
def get_room(room_id):
    room = list(filter(lambda t: t['id'] == room_id, rooms))
    if len(room) == 0:
        abort(404)

    print(request.headers)
    return jsonify({'room': room[0]})


@app.route('/objects/', methods=['GET'])
def get_objects():
    print(request.headers)

    return jsonify({'objects': objects})


@app.route('/messages/', methods=['POST'])
def post_message():
    print(request.headers)
    print(request.get_data())
    print(request.get_json())
    return "accepted", 202


@app.route('/objects/<string:object_id>', methods=['GET'])
def get_object(object_id):
    object_item = list(filter(lambda t: t['id'] == object_id, objects))
    if len(object_item) == 0:
        abort(404)

    print(request.headers)
    return jsonify({'object': object_item[0]})

if __name__ == '__main__':
    app.run(debug=True, port=10800)


