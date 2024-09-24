import json

from flask import Flask, jsonify, request

from model.twit import Twit

twits = []

app = Flask(__name__)

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Twit):
            return {'body': obj.body, 'author': obj.author}
        else:
            return super().default(obj)

app.json_encoder = CustomJSONEncoder
@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'response': 'pong'})

@app.route('/twit', methods=['POST'])
def create_twit():
    '''
    {"body": "Hello World", "author": "Nel"}
    '''
    twit_json = request.get_json()  # Use request.get_json() to retrieve JSON data from the request
    if not twit_json or 'body' not in twit_json or 'author' not in twit_json:
        return jsonify({'error': 'Invalid input'}), 400  # Validate input and return an error if it's invalid
    twit = Twit(twit_json['body'], twit_json['author'])
    twits.append(twit)
    return jsonify({'status': 'success'})

@app.route('/twit', methods=['GET'])
def read_twit():
    twits_list = [{'body': twit.body, 'author': twit.author} for twit in twits]
    return jsonify({'twits': twits_list})

if __name__ == '__main__':
    app.run(host = 'localhost', port = 5000, debug=True)