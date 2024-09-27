import json

from flask import Flask, jsonify, request

from model.post import Post
from model.user import User

users = []
posts = []

app = Flask(__name__)

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Post):
            return {'body': obj.body, 'author': obj.author}
        elif isinstance(obj, User):
            return {'username': obj.username, 'posts': [post.body for post in obj.posts]}
        else:
            return super().default(obj)

app.json_encoder = CustomJSONEncoder

@app.route('/user', methods=['POST'])
def create_user():
    '''
    {"username": "User"}
    '''
    user_json = request.get_json()
    if not user_json or 'username' not in user_json:
        return jsonify({'error': 'Invalid input'})

    new_user = User(user_json['username'])
    users.append(new_user)
    return jsonify({'status': 'User created successfully'})

@app.route('/user/<username>', methods=['GET'])
def get_user(username):
    for user in users:
        if user.username == username:
            return jsonify(user)
    return jsonify({'error': 'User not found'})

@app.route('/post', methods=['POST'])
def create_post():
    '''
    {"body": "Text", "author": "User"}
    '''
    post_json = request.get_json()
    if not post_json or 'body' not in post_json or 'author' not in post_json:
        return jsonify({'error': 'Invalid input'})

    author = next((user for user in users if user.username == post_json['author']), None)
    if not author:
        return jsonify({'error': 'Author not found'})

    new_post = Post(post_json['body'], post_json['author'])
    author.posts.append(new_post)
    posts.append(new_post)
    return jsonify({'status': 'Post created successfully'})

@app.route('/post', methods=['GET'])
def read_posts():
    post_list = [{'body': post.body, 'author': post.author} for post in posts]
    return jsonify({'posts': post_list})

@app.route('/post/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    if post_id >= len(posts) or post_id < 0:
        return jsonify({'error': 'Post not found'})

    post_to_delete = posts[post_id]
    author = next((user for user in users if user.username == post_to_delete.author), None)
    if author:
        author.posts.remove(post_to_delete)

    posts.pop(post_id)
    return jsonify({'message': 'Post deleted successfully'})

@app.route('/post/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    '''
    {"body": "Updated text", "author": "User"}
    '''
    if post_id >= len(posts) or post_id < 0:
        return jsonify({'error': 'Post not found'})

    post_json = request.get_json()
    if not post_json or 'body' not in post_json:
        return jsonify({'error': 'Invalid input'})

    post_to_update = posts[post_id]
    if post_to_update.author != post_json.get('author'):
        return jsonify({'error': 'Author mismatch'})

    post_to_update.body = post_json['body']
    return jsonify({'status': 'Post updated successfully'})


if __name__ == '__main__':
    app.run(host = 'localhost', port = 5000, debug=True)