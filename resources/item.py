from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type = float,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('store_id',
        type = float,
        required=True,
        help="Every item needs a store id!"
    )

    # @jwt_required()
    def get(self, name):
        #item = next(filter(lambda  x:x['name'] == name, items), None)
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message':'Item not found'},404    

    def post(self,name):        
        #Verify if item extist
        if ItemModel.find_by_name(name):
            return {'message':"An item with the name '{}' already exist".format(name)}, 400

        data = Item.parser.parse_args()
        item = ItemModel(None,name, data['price'], data['store_id'])
        #items.append(item)
        try:
            item.save_to_db()
        except:
            return {'message', 'An error ocurred inserting item.'}, 500

        return item.json(),201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        #updated_item = ItemModel(name,data['price'])
        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']

        item.save_to_db()
        
        return updated_item.json()


class ItemList(Resource):
    #@jwt_required()
    def get(self):
        return {'item':  [item.json() for item in ItemModel.query.all()]}