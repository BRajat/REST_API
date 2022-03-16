import sqlite3

class UserModel:
    
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
