from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

# Path to the posts JSON file
POSTS_FILE = 'posts.json'

# Function to read posts from the JSON file
def read_posts():
    if not os.path.exists(POSTS_FILE):
        return []
    with open(POSTS_FILE, 'r') as f:
        return json.load(f)

# Function to write posts to the JSON file
def write_posts(posts):
    with open(POSTS_FILE, 'w') as f:
        json.dump(posts, f)

@app.route('/api/posts', methods=['GET', 'POST'])
def posts():
    if request.method == 'POST':
        data = request.get_json()
        posts = read_posts()
        new_post = {
            'content': data['content'],
            'fileLink': data.get('fileLink', '')
        }
        posts.append(new_post)
        write_posts(posts)
        return jsonify(new_post), 201
    else:
        return jsonify(read_posts()), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
