from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from src.security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'venkatram'
api = Api(app)

jwt = JWT(app, authenticate, identity)

items = []

class Item(Resource):

    # def get(self, name):
    #     for item in items:
    #         if item['name'] == name:
    #             return item
    #     return {'item': None}, 404

    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)

        return {'item': item}, 200 if item is not None else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'message':"An item with name '{}' already exists.".format(name)}, 400
        data = request.get_json()   #silent=True, or force=True
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return items, 201

    def delete(self, name):
        global items  #we have use global, then it refers items, or else, which is the local items variable
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Item deleted'}

    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument('price',
            type=float,
            required=True,
            help="This field can not be left blank."
        )
        data = parser.parse_args()#request.get_json()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
            items.append(item)
        return item


class ItemList(Resource):
    def get(self):
        return {'items': items}



api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)

