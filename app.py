from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList
import os

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#secret_key is used to encrypt the userid
app.secret_key = "karnawat"

jwt = JWT(app, authenticate, identity)


api.add_resource(Item, '/item/<string:name>') #http://localhost:5000/item/chair
api.add_resource(ItemList, '/items') #http://localhost:5000/items
api.add_resource(UserRegister, '/register') #http://localhost:5000/register
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/store/storelist')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
