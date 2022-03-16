from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3
from models.item import ItemModel

class Item(Resource):
    TABLE_NAME = 'items'

    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message':'Item not found'}, 404
  
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message':'An item {} already exists'.format(name)}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, data['price'])
        # items.append(item) ---> only useful for case when items are in list, now we want to post item to database
        try:
            item.insert()
        except:
            return {"message": "An error occurred inserting the item."}

        return item.json(), 201

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item is None:
            return {'message':'Item not in database'}

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM {table} WHERE name=?".format(table=self.TABLE_NAME)
        cursor.execute(query, (name,))
        
        connection.commit()
        connection.close()
        
        return {'message': 'Item deleted'}

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        # Once again, print something not in the args to verify everything works
        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name,data['price'])
        if item is None:
            try:
                updated_item.insert()        # if absent - insert
            except:
                return {'message':'An error occured inserting'}
        else:
            try:
                updated_item.update()    # if present - update
            except:
                return {'message':'An error occured updating'}
        return updated_item.json()

    
class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name':row[0],'price':row[1]})

        connection.close()

        return {'items':items}

