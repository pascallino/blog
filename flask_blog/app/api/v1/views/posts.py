#!/usr/bin/python3
"""Create a new view for User object that
handles all default RESTFul API actions:"""

from sqlalchemy import *
from sqlalchemy.orm import *
from flask import abort, jsonify, make_response, request
from api.v1.views.path import app_views
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models import *

def serialized_posts(post):
    """Serialize a User object to a JSON-serializable format."""
    return {
        'post_id': post.postid,
        'title': post.title,
        'user_id': post.user_id,
        'filepath': post.filepath,
        'created': post.created,
        'body': post.body,
        'slug': post.slug,

        # Add other User attributes here
    }

@app_views.route('/users/<user_id>/posts', methods=['GET'],
                 strict_slashes=False)
# @jwt_required()
def get_posts_by_userId(user_id):
    """
    Retrieves the list of all posts objects
    of a specific User, or a specific user
    """
#    current_user = get_jwt_identity()
#    if not current_user:
#        return jsonify({"message": "Not a valid user"}), 401
#    user = User.query.filter_by(email=current_user).first()
#    if not user:
#        return jsonify({"message": "Not a valid user"}), 401

    list_posts = []
    user = User.query.filter_by(userid=user_id).first()
    if not user:
        abort(404)
    for post in user.posts:
        list_posts.append(serialized_posts(post))
    return jsonify(list_posts)

@app_views.route('/posts', methods=['GET'], strict_slashes=False)
# @jwt_required()
def get_posts():
    """get all posts"""
    # current_user = get_jwt_identity()
    # if not current_user:
    #    return jsonify({"message": "Not a valid user"}), 401
    # user = User.query.filter_by(email=current_user).first()
    # if not user:
    #     return jsonify({"message": "Not a valid user"}), 401

    posts = Post.query.order_by(Post.created.desc())
    serialized_post = [serialized_posts(post) for post in posts]
    return jsonify(serialized_post)

@app_views.route('/posts/<id>', methods=['GET'], strict_slashes=False)
def get_post_by_id(id):
    """get post by id"""
    # users = []
    post = Post.query.filter_by(postid=id).first()
    if post is None:
        abort(404)
    serialized_post = serialized_posts(post)
    return jsonify(serialized_post)

@app_views.route('/posts/<id>', methods=['DELETE'],
                 strict_slashes=False)
@jwt_required()
def delete_post(id):
    """Delete a post by id"""
    current_user = get_jwt_identity()
    if not current_user:
        return jsonify({"message": "Not a valid user"}), 401
    user = User.query.filter_by(email=current_user).first()
    if not user:
        return jsonify({"message": "Not a valid user"}), 401

    post = Post.query.filter_by(postid=id).first()
    if post is None:
        abort(404)
    db.session.delete(post)
    db.session.commit()
    return (jsonify({}))

@app_views.route('/users/<user_id>/posts', methods=['POST'], strict_slashes=False)
@jwt_required()
def post_blog(user_id):
    """Create a post for a specific user"""
    current_user = get_jwt_identity()
    if not current_user:
        return jsonify({"message": "Not a valid user"}), 401
    user = User.query.filter_by(email=current_user).first()
    if not user:
        return jsonify({"message": "Not a valid user"}), 401

    user = User.query.filter_by(userid=user_id).first()
    if not user:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'title' not in request.get_json():
        return make_response(jsonify({'error': 'Missing title'}), 400)
    if 'body' not in request.get_json():
        return make_response(jsonify({'error': 'Missing body'}), 400)
    post = Post(**request.get_json())
    post.user_id = user.userid
    db.session.add(post)
    db.session.commit()
    return make_response(jsonify(serialized_posts(post)), 201)

@app_views.route('/posts/<id>', methods=['PUT'],
                 strict_slashes=False)
@jwt_required()
def put_post(id):
    """update post """
    current_user = get_jwt_identity()
    if not current_user:
        return jsonify({"message": "Not a valid user"}), 401
    user = User.query.filter_by(email=current_user).first()
    if not user:
        return jsonify({"message": "Not a valid user"}), 401

    post = Post.query.filter_by(postid=id).first()
    if post is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'user_id', 'created', 'slug']:
            setattr(post, attr, val)
    db.session.commit()
    return jsonify(serialized_posts(post))