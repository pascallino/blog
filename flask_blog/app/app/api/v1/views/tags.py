#!/usr/bin/python3
"""Create a new view for tag object that
handles all default RESTFul API actions:"""

from sqlalchemy import *
from sqlalchemy.orm import *
from flask import abort, jsonify, make_response, request
from api.v1.views.path import app_views
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models import *

def serialized_tags(tag):
    """Serialize a tag object to a JSON-serializable format."""
    return {
        'tag_id': tag.tagid,
        'title': tag.title,
        'slug': tag.slug,
        'created': tag.created,
        # Add other User attributes here
    }


@app_views.route('/tags/<tag_id>/posts', methods=['GET'],
                 strict_slashes=False)
def get_posts_by_tagId(tag_id):
    """
    Retrieves the list of all tags objects
    of a specific tags, or a specific user
    """
    list_tags = []
    tag = Tag.query.filter_by(tagid=tag_id).first()
    if not tag:
        abort(404)
    for post in tag.posts:
        list_tags.append(serialized_tags(post))
    return jsonify(list_tags)

@app_views.route('/tags', methods=['GET'], strict_slashes=False)
def get_tags():
    """Create a new view for tags object that handles
    all default RESTFul API actions:"""
    # users = []
    tags = Tag.query.order_by(Tag.id.desc())
    serialized_tag = [serialized_tags(tag) for tag in tags]
    return jsonify(serialized_tag)

@app_views.route('/tags/<id>', methods=['GET'], strict_slashes=False)
def get_tag_by_id(id):
    """Create a new view for tags object that handles
    all default RESTFul API actions:"""
    # users = []
    tag = Tag.query.filter_by(tagid=id).first()
    if tag is None:
        abort(404)
    serialized_tag = serialized_tags(tag)
    return jsonify(serialized_tag)

@app_views.route('/tags/<id>', methods=['DELETE'],
                 strict_slashes=False)
@jwt_required()
def delete_tag(id):
    """Create a new view for tag object that
    handles all default RESTFul API actions:"""
    current_user = get_jwt_identity()
    if not current_user:
        return jsonify({"message": "Not a valid user"}), 401
    user = User.query.filter_by(email=current_user).first()
    if not user:
        return jsonify({"message": "Not a valid user"}), 401

    tag = Tag.query.filter_by(tagid=id).first()
    if tag is None:
        abort(404)
    db.session.delete(tag)
    db.session.commit()
    return (jsonify({}))

@app_views.route('posts/<post_id>/tags/<tag_id>', methods=['POST'], strict_slashes=False)
@jwt_required()
def create_posts_tags(post_id, tag_id):
    """Create a new view for tag object
    that handles all default RESTFul API actions:"""
    current_user = get_jwt_identity()
    if not current_user:
        return jsonify({"message": "Not a valid user"}), 401
    user = User.query.filter_by(email=current_user).first()
    if not user:
        return jsonify({"message": "Not a valid user"}), 401

    post = Post.query.filter_by(postid=post_id).first()
    if not post:
        abort(404)
    tag = Tag.query.filter_by(tagid=tag_id).first()
    if not tag:
        abort(404)
    if tag in post.tags:
        return make_response(jsonify(serialized_tags(tag)), 200)
    else:
        post.tags.append(tag)
        tag.posts.append(post)

    db.session.commit()
    return make_response(jsonify(serialized_tags(tag)), 201)


@app_views.route('/tags', methods=['POST'], strict_slashes=False)
@jwt_required()
def post_tag():
    """Create a new view for Tag object
    that handles all default RESTFul API actions:"""
    current_user = get_jwt_identity()
    if not current_user:
        return jsonify({"message": "Not a valid user"}), 401
    user = User.query.filter_by(email=current_user).first()
    if not user:
        return jsonify({"message": "Not a valid user"}), 401

    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'title' not in request.get_json():
        return make_response(jsonify({'error': 'Missing title'}), 400)
    tag = Tag(**request.get_json())
    db.session.add(tag)
    db.session.commit()
    return make_response(jsonify(serialized_tags(tag)), 201)

@app_views.route('/tags/<id>', methods=['PUT'],
                 strict_slashes=False)
@jwt_required()
def put_tag(id):
    """Create a new view for tag object that
    handles all default RESTFul API actions:"""
    current_user = get_jwt_identity()
    if not current_user:
        return jsonify({"message": "Not a valid user"}), 401
    user = User.query.filter_by(email=current_user).first()
    if not user:
        return jsonify({"message": "Not a valid user"}), 401

    tag = Tag.query.filter_by(tagid=id).first()
    if tag is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'slug','created']:
            setattr(tag, attr, val)
    db.session.commit()
    return jsonify(serialized_tags(tag))