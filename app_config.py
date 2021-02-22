from flask import Flask, request
from flask_restful import Api
from flask_caching import Cache
# import redis


# initialize flask instance
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.secret_key = 'kreeda' # app.config['JWT_SECRET_KEY']

# initialize api
api = Api(app)

# initialize redis cache
cache = Cache(app, config={'CACHE_TYPE': 'redis'})

def make_cache_key(*args, **kwargs):
    return request.url
