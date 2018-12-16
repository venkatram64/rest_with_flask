from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from salchemy.models.item import ItemModel
import sqlite3

class Item(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be blank."
    )

    @jwt_required()
    def get(self, name):

        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        else:
            return {'message': 'Item not found'}, 404



    def post(self, name):

        row = ItemModel.find_by_name(name)
        if row is not None:
            return {'message': "An item with name '{}' already exists.".format(name)}, 400
        data = Item.parser.parse_args()   #silent=True, or force=True

        item = ItemModel(name, data['price'])
        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred while inserting."}, 500
        return item.json(), 201


    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args() #request.get_json()
        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, data['price'])
        else:
            item.price = data['price']

        item.save_to_db()
        return item.json()


class ItemList(Resource):

    def get(self):
        #return {'items': [item.json() for item in ItemModel.query.all()]}
        return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
