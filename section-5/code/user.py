import sqlite3
from flask_restful import Resource, reqparse

class User:
    
    TABLE_NAME = 'users'
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    def __repr__(self):
        return 'User({},{},{})'.format(self.id, self.username, self.password)

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * from {table} where username = ?'.format(table=cls.TABLE_NAME)
        result = cursor.execute(query, (username,))

        row = cursor.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
    
        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * from {table} where id = ?'.format(table = cls.TABLE_NAME)
        result = cursor.execute(query, (_id,))

        row = cursor.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
    
        connection.close()
        return user


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

        if User.find_by_username(data['username']):
            return {'message':'user already exist'},400

        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data['username'],data['password']))

        connection.commit()
        connection.close()

        return {'messsage':'user created successfully'}, 201
