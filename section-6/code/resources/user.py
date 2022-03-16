import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type = str,
        required = True,
        help = 'This cannot be blank'
    )
    parser.add_argument('password',
        type = str,
        required = True,
        help = 'This cannot be blank'
    )

    def post(self):
        data = UserRegister.parser.parse_args()
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        if UserModel.find_by_username(data['username']):
            return {'message':'user already exist'},400

        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data['username'],data['password']))

        connection.commit()
        connection.close()

        return {'messsage':'user created successfully'}, 201
