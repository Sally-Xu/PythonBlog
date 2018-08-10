from app import db, bcrypt
from models import Post, PostSchema, User
from flask import current_app, jsonify, Blueprint, request
from flask_login import login_required, current_user

from datetime import datetime, timedelta
import jwt
from functools import wraps
from api.util import token_required

api = Blueprint('api', __name__)

@api.route('/api/posts', methods=['GET'])
def get_posts():
    # posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page = 5, page = 1)
    posts = Post.query.order_by(Post.date_posted.desc())
    return  PostSchema(many=True).jsonify(posts)

@api.route('/api/post/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.get(post_id)
    if (post is None):
        return jsonify({'message': 'No record found'})
    return PostSchema(many=False).jsonify(post)

@api.route('/api/user/<int:user_id>/posts', methods=['GET'])
@token_required
def get_userposts(current_user, user_id):
    user = User.query.get_or_404(user_id)
    user_posts = Post.query.filter_by(author=user)
    return  PostSchema(many=True).jsonify(user_posts)

@api.route('/api/post/<int:post_id>/del', methods=['DELETE'])
@token_required
def del_post(current_user, post_id):
    post = Post.query.get(post_id)
    if (post is None):
        return jsonify({'message': 'No record found'})
    if (post.author != current_user):
        return jsonify({'message': 'You do not have permission to delete this record'})

    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': 'The post has been deleted'})


@api.route('/api/login', methods=['GET'])
def login():
    auth = request.authorization
    if (not auth or not auth.username or not auth.password):
        return make_response("Could not verify", 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    user = User.query.filter(User.email.ilike(auth.username)).first()
    
    if not user:
        return make_response("Could not verify", 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    
    if not bcrypt.check_password_hash(user.password, auth.password):
         return make_response("Could not verify", 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    token = jwt.encode({'id': user.id, 'exp': datetime.utcnow() + timedelta(minutes=30) }, current_app.config['SECRET_KEY'])
    return jsonify({'token':token.decode('UTF-8')})
   
    

