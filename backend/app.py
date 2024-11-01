from flask import Flask, request, jsonify
import uuid
import os
import json

app = Flask(__name__)

# Path to store posts
POSTS_FILE = 'posts.json'

# Load existing posts from JSON file
def load_posts():
    if os.path.exists(POSTS_FILE):
        with open(POSTS_FILE, 'r') as f:
            return json.load(f)
    return []

# Save posts to JSON file
def save_posts(posts):
    with open(POSTS_FILE, 'w') as f:
        json.dump(posts, f)

@app.route('/api/posts', methods=['GET', 'POST'])
def posts():
    if request.method == 'POST':
        data = request.json
        post_id = str(uuid.uuid4())
        post = {
            'id': post_id,
            'content': data['content'],
            'file_link': data.get('file_link'),
            'likes': 0,
            'timestamp': data.get('timestamp')
        }
        posts = load_posts()
        posts.append(post)
        save_posts(posts)
        return jsonify(post), 201

    posts = load_posts()
    return jsonify(posts), 200

if __name__ == '__main__':
    app.run(debug=True)
