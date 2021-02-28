from flask import Flask, request
from flask_restful import Api
from flask_caching import Cache
# import redis


# initialize flask instance
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.secret_key =  # manually removed this, To Do: move to a config file and add to .gitignore

# initialize api
api = Api(app)

# initialize redis cache
cache = Cache(app, config={'CACHE_TYPE': 'redis'})

def make_cache_key(*args, **kwargs):
    return request.url
