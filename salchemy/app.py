from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from salchemy.security import authenticate, identity
from salchemy.resources.user import UserRegister
from salchemy.resources.item import ItemList, Item

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'venkatram'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from salchemy.db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
