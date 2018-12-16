from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from sqlite.models.item import ItemModel
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
            item.insert()
        except:
            return {"message": "An error occurred while inserting."}, 500
        return item.json(), 201


    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "DELETE from items WHERE name=?"
        cursor.execute(query, (name,))
        connection.commit()
        connection.close()
        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args() #request.get_json()
        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name, data['price'])
        if item is None:
            try:
                updated_item.insert()
            except:
                return {"message": "An error occurred while inserting the item."}, 500
        else:
            try:
                updated_item.update()
            except:
                return {"message": "An error occurred while updating the item."}, 500
        return updated_item.json()


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []
        for tuple in result:
            items.append({'name': tuple[0], 'price': tuple[1]})

        connection.close()
        return {'items': items}