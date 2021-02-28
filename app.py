from flask import jsonify
from flask_jwt_extended import JWTManager

from resources.user import UserRegister, User, UserLogin, UserLogout, TokenRefresh
from resources.category import Category, CategoryList
from resources.category_item import CategoryItem, CategoryItemList
from resources.twitter_stream import TwitterStream
from models.tweet import TweetModel

from blacklist import BLACKLIST
from app_config import app, api


@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWTManager(app)  # not creating /auth

@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1: # To Do: instead of hard-coding, read from a config file or a database
        return {'is_admin': True}
    return {'is_admin': False}

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST

@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'description': 'The token has expired',
        'error': 'expired_token'
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'description': 'Signature verification failed',
        'error': 'invalid_token'
    }), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'description': 'Request does not contain an access token',
        'error': 'authorization_required'
    }), 401

@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        'description': 'The token is not fresh',
        'error': 'fresh_token_required'
    }), 401

@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'description': 'The token has been revoked',
        'error': 'token_revoked'
    }), 401


api.add_resource(TwitterStream, '/twitter-stream')
api.add_resource(Category, '/category/<string:name>')
api.add_resource(CategoryList, '/categories')
api.add_resource(CategoryItem, '/category-item/<string:name>')
api.add_resource(CategoryItemList, '/category-items')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, '/refresh')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
