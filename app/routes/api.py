from flask import Blueprint, jsonify, request
from app.models.posts import Post
from app.models.user import User
from app.extensions import db
from flask_login import login_required, current_user
api = Blueprint('api', __name__)

@api.route('/posts/<int:id>', methods=['GET'])
def get_post(id):
    post = Post.query.get_or_404(id)
    return jsonify({
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'author': post.author.username
    })

@api.route('/posts', methods=['GET'])
def list_posts():
    posts = Post.query.all()
    posts_data = [{
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'author': post.author.username
    } for post in posts]
    return jsonify(posts_data)

@api.route('/posts', methods=['POST'])
@login_required
def create_post():
    data = request.get_json()
    new_post = Post(
        title=data['title'],    
        content=data['content'],
        author_id=current_user
    )
    try:
        db.session.add(new_post)
        db.session.commit()
        return jsonify({'message': 'Post created', 'id': new_post.id}), 201
    except Exception as e:
        db.session.rollback()
        
    return jsonify({'message': 'Post created', 'id': new_post.id}), 201

@api.route('/posts/<int:id>', methods=['PUT'])
@login_required
def update_post(id):
    post = Post.query.get_or_404(id)
    if post.author != current_user:
        return jsonify({'message': 'Unauthorized'}), 403
    
    data = request.get_json()
    post.title = data.get('title', post.title)
    post.content = data.get('content', post.content)
    try:
        db.session.commit()
        return jsonify({'message': 'Post updated'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error updating post'}), 500

@api.route('/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    post = Post.query.get_or_404(id)
    try:
        db.session.delete(post)
        db.session.commit()
        return jsonify({'message': 'Post deleted'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error deleting post'}), 500    

@api.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email
    })