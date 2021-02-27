import random
import tweepy
from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required, 
    get_jwt_claims, 
    jwt_optional, 
    get_jwt_identity,
    fresh_jwt_required
)
from models.category import CategoryModel
from models.category_item import CategoryItemModel
from app_config import cache, make_cache_key
from twitter.twitter_filter import StreamListener, api


class TwitterStream(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('category',
                        type=str,
                        required=True,
                        help="A category is required."
                        )
    parser.add_argument('category_items',
                        type=str,
                        action='append',
                        required=True,
                        help="A list of category items is required."
                        )

    @jwt_required
    # @cache.cached(timeout=5, key_prefix=make_cache_key)
    def get(self, name):
        # get tweets for a particular category item
        return {'message': 'Tweets not found'}, 404

    @jwt_required
    def post(self):
        data = TwitterStream.parser.parse_args()
        new_category = None

        # check if the category already exists, if not create it
        category = CategoryModel.find_by_name(data['category'])
        if not category:
            new_category = CategoryModel(data['category'])
            try:
                new_category.save_to_db()
            except:
                return {
                    "message": "An error occurred inserting the category."
                }, 500

        category_id = category.id if category else new_category.id

        # check if the category items already exists, if not create them
        for item_name in data['category_items']:
            if not CategoryItemModel.find_by_name(item_name):
                category_item = CategoryItemModel(item_name, category_id)
                try:
                    category_item.save_to_db()
                except:
                    return {
                        "message": "An error occurred inserting the category item."
                    }, 500

        # WIP:
        # Trigger the twitter filter stream listener below
        stream_listener = StreamListener()
        stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
        stream.filter(track=[item for item in data['category_items']])


        return 200
