from flask import request
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):

    parser = reqparse.RequestParser();
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field can't be left blank!"
    )

    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every item requires a store id"
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_itemname(name)
        return item.json(), 200 if item is not None else 404



    def post(self,name):
        if( ItemModel.find_by_itemname(name)):
            return {"message": "An item with name {} already exists".format(name)},400
        request_data = Item.parser.parse_args()
        #request_data = request.get_json()
        item = ItemModel(name, request_data['price'], request_data['store_id'])
        try:
            item.save_to_db()
        except:
            return {"message":"An error occured in adding the item"}, 500
        return item.json(),201


    def delete(self, name):
        item = ItemModel.find_by_itemname(name)
        if item:
            item.delete_from_db()
        return {'message': 'item deleted from items!'}, 200

    def put(self, name):
        request_data = Item.parser.parse_args()
        #request_data = request.get_json()
        updated_item = ItemModel.find_by_itemname(name)
        if(updated_item):
            try:
                updated_item.price = request_data['price']
                updated_item.save_to_db();
            except:
                return {'message':'An error occured'},500
        else:
            try:
                updated_item = ItemModel(name, request_data['price'])
                updated_item.save_to_db()
            except:
                return {'message':'An error occured'},500

        return updated_item.json()



class ItemList(Resource):
    def get(self):
        return {"items": [item.json() for item in ItemModel.query.all()]}
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        result = cursor.execute('SELECT * FROM items')
        items = []
        for row in result:
            items.append({'item':row[0], 'price':row[1]})
        connection.close()
        return {"items": items}
