import random
from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required, 
    get_jwt_claims, 
    jwt_optional, 
    get_jwt_identity,
    fresh_jwt_required
)
from models.category_item import CategoryItemModel
from app_init import cache, make_cache_key


class CategoryItem(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('category_id',
                        type=int,
                        required=True,
                        help="Every category item needs a category_id."
                        )

    @jwt_required
    # @cache.cached(timeout=5, key_prefix=make_cache_key)
    def get(self, name):
        category_item = CategoryItemModel.find_by_name(name)
        # below is just for practicing caching
        # item.price = random.randint(0,100)
        if category_item:
            return category_item.json()
        return {'message': 'Item not found'}, 404

    @fresh_jwt_required
    def post(self, name):
        if CategoryItemModel.find_by_name(name):
            return {'message': "A category item with name '{}' already exists.".format(name)}, 400
        data = CategoryItem.parser.parse_args()
        category_item = CategoryItemModel(name, **data)
        try:
            category_item.save_to_db()
        except:
            return {"message": "An error occurred inserting the category item."}, 500

        return category_item.json(), 201

    @jwt_required
    def delete(self, name):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required'}, 401

        category_item = CategoryItemModel.find_by_name(name)
        if category_item:
            category_item.delete_from_db()
            return {'message': 'Category item deleted.'}
        return {'message': 'Category item not found.'}, 404

    def put(self, name):
        data = CategoryItem.parser.parse_args()
        category_item = CategoryItemModel.find_by_name(name)

        if category_item:
            category_item.price = data['price']
        else:
            category_item = CategoryItemModel(name, **data)

        category_item.save_to_db()

        return category_item.json()


class CategoryItemList(Resource):
    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()
        category_items = [
            category_item.json() for category_item in CategoryItemModel.find_all()
        ]
        if user_id:
            return {'category_items': category_items}, 200
        return {
            'category_items': [
                category_item['name'] for category_item in category_items
            ],
            'message': 'More data available if you login'
        }, 200
