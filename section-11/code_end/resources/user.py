from flask_restful import Resource, reqparse
from flask_jwt_extended import ( create_access_token, 
                                 create_refresh_token,
                                 get_jwt_identity,
                                 jwt_required,
                                 get_jti
                                )
from werkzeug.security import safe_str_cmp

from blacklist import BLACKLIST
from models.user import UserModel

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                            type = str,
                            required = True,
                            help = 'This cannot be blank'
                            )
_user_parser.add_argument('password',
                                type = str,
                                required = True,
                                help = 'This cannot be blank'
                                )

# defines endpoint to register user
class UserRegister(Resource):
    

    def post(self):
        data = _user_parser.parse_args()
        
        if UserModel.find_by_username(data['username']):
            return {'message':'user already exist'},400

        user = UserModel(**data)
        user.save_to_db()

        return {'messsage':'user created successfully'}, 201

# defines endpoint to access user given user_id
class User(Resource):

    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message':'User not found'} , 404
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message':'User not found'}, 404
        user.delete_from_db()
        return {'message':'User deleted'}, 200
    

# Since, we are no longer using security.py - 'authenticate' and 'identity' methods
# We have to create UserLogin Endpoint for this

# defines endpoint for user to login
class UserLogin(Resource): 

    # using post method to authenticate 
    def post(cls):
        
        # get data from parser
        data = _user_parser.parse_args()

        # find username
        user = UserModel.find_by_username(data['username'])
    
        # check if password matches
        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh= True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token':access_token,
                'refresh_token': refresh_token
            }, 200
        
        return {'message': 'Invalid credentials'}, 401

class UserLogout(Resource):

    @jwt_required
    def post(self):
        jti = get_jti()
        user_id = get_jwt_identity()
        BLACKLIST.add(jti)
        return {"message": "User <id={}> successfully logged out.".format(user_id)}, 200
        
# new resource - calling which gives us new refreshed token
class RefreshToken(Resource):

    @jwt_required(refresh = True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        
        return {'access_token':new_token}, 200

        


