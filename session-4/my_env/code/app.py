import re
from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

app = Flask(__name__)                              # 
app.secret_key = 'cool'
api = Api(app)

jwt = JWT(app, authenticate, identity)             # creates new endpoint ; auth

items=[]

class Item(Resource):

    # def get
    @jwt_required() 
    def get(self,name):
        for item in items:
            if item['name'] == name:
                return item
        return {'item':None},401

    def post(self,name):
        data = request.get_json()
        item = {'name':name, 'price':data['price']}
        items.append(item)
        return item, 200


    def put(self,name):
        pass

    def delete(self,name):
        pass


class ItemList(Resource):
    # list all items
    def get(self):
        return {'items':items}


# define endpoints for api
api.add_resource(Item, '/item/<string:name>')        # endpoint for get or post particular item
api.add_resource(ItemList, '/items')                 # endpoint to get all items

# run the flask app
app.run(port = 5000, debug= True)