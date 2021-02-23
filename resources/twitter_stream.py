import random
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

        # TO DO:
        # create the messages to be sent out via rabbitMQ and add them to a task queue

        

        return 200



# class CategoryItemList(Resource):
#     @jwt_optional
#     def get(self):
#         user_id = get_jwt_identity()
#         category_items = [
#             category_item.json() for category_item in CategoryItemModel.find_all()
#         ]
#         if user_id:
#             return {'category_items': category_items}, 200
#         return {
#             'category_items': [
#                 category_item['name'] for category_item in category_items
#             ],
#             'message': 'More data available if you login'
#         }, 200
