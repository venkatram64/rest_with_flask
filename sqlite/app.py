from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from sqlite.security import authenticate, identity
from sqlite.resources.user import UserRegister
from sqlite.resources.item import ItemList, Item

app = Flask(__name__)
app.secret_key = 'venkatram'
api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    app.run(port=5000, debug=True)

