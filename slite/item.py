from flask import request
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3

class Item(Resource):

    parser = reqparse.RequestParser()
    # parser.add_argument('name',
    #     type=str,
    #     required=True,
    #     help="This field cannot be blank."
    # )

    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be blank."
    )

    @jwt_required()
    def get(self, name):

        row = Item.find_by_name(name)
        if row:
            return {'item': {'name': row[0], 'price': row[1]}}
        else:
            return {'message': 'Item not found'}, 404

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()
        return row

    def post(self, name):
        row = Item.find_by_name(name)
        if row is not None:
            return {'message': "An item with name '{}' already exists.".format(name)}, 400
        data = Item.parser.parse_args()   #silent=True, or force=True

        item = {'name': name, 'price': data['price']}
        try:
            self.insert(item)
        except:
            return {"message": "An error occurred while inserting."}, 500
        return item, 201

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO items VALUES(?, ?)"
        cursor.execute(query, (item['name'], item['price']))
        connection.commit()
        connection.close()

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['price'], item['name']))
        connection.commit()
        connection.close()

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
        item = self.find_by_name(name)
        updated_item = {'name': name, 'price': data['price']}
        if item is None:
            try:
                self.insert(updated_item)
            except:
                return {"message": "An error occurred while inserting the item."}, 500
        else:
            try:
                self.update(updated_item)
            except:
                return {"message": "An error occurred while updating the item."}, 500
        return updated_item


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