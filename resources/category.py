import random
from flask_restful import Resource
from models.category import CategoryModel
from app_config import cache, make_cache_key


class Category(Resource):
    # @cache.cached(timeout=5, key_prefix=make_cache_key)
    def get(self, name):
        category = CategoryModel.find_by_name(name)
        if category:
            # below is just for manually testing cache
            # store.name = store.name + str(random.randint(0,100))
            return category.json()
        return {'message': 'Category not found'}, 404

    def post(self, name):
        if CategoryModel.find_by_name(name):
            return {'message': "A category with name '{}' already exists.".format(name)}, 400

        category = CategoryModel(name)
        try:
            category.save_to_db()
        except:
            return {"message": "An error occurred creating the category."}, 500

        return category.json(), 201

    def delete(self, name):
        category = CategoryModel.find_by_name(name)
        if category:
            category.delete_from_db()

        return {'message': 'Category deleted'}


class CategoryList(Resource):
    def get(self):
        return {'categories': [x.json() for x in CategoryModel.find_all()]}
