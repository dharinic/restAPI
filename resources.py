from flask_restful import Resource, reqparse
from models import UserModel
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)


parser = reqparse.RequestParser()
parser.add_argument('username', help = 'This field cannot be blank', required = True)
parser.add_argument('password', help = 'This field cannot be blank', required = True)



USER_DATA = {
    "admin": "pass"
}

@auth.verify_password
def verify(username, password):
    if not (username and password):
       return False
    return USER_DATA.get(username) == password


users = [
    {
        "name": "Nicholas",
        "age": 42,
        "occupation": "Network Engineer"
    },
    {
        "name": "Elvin",
        "age": 32,
        "occupation": "Doctor"
    },
    {
        "name": "Jass",
        "age": 22,
        "occupation": "Web Developer"
    }
]

class UserReg(Resource):
    def post(self):
        #parser = reqparse.RequestParser()
        args = parser.parse_args()
        new_user = UserModel(
            username = args['username'],
            password = UserModel.generate_hash(args['password'])
        )
        try:
            new_user.save_to_db()
            access_token = create_access_token(identity = args['username'])
            refresh_token = create_refresh_token(identity = args['username'])
            return {
                'message': 'created User {}  '.format( args['username']),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        except:
            return {'message': 'failed to create user'}, 500

class UserLogin(Resource):
    def post(self):
        data = parser.parse_args()
        current_user = UserModel.find_by_username(data['username'])
        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['username'])}

        if UserModel.verify_hash(data['password'], current_user.password):
            access_token = create_access_token(identity = data['username'])
            refresh_token = create_refresh_token(identity = data['username'])
            return {'message': 'Logged in as {}'.format(current_user.username),'access_token': access_token,
                'refresh_token': refresh_token}
        else:
            return {'message': 'Wrong credentials'}

class SecretResource(Resource):
    @jwt_required
    def get(self):
        return {
            'message': 'Token authorized'}

class User(Resource):
    @auth.login_required
    def get(self, name):
        for user in users:
            if(name == user["name"]):
                return user, 200
        return "User not found", 404

    def post(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("age")
        parser.add_argument("occupation")
        args = parser.parse_args()

        for user in users:
            if(name == user["name"]):
                return "User with name {} already exists".format(name), 400
        user = {
            "name": name,
            "age": args["age"],
            "occupation": args["occupation"]
        }
        users.append(user)
        return user, 201

    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("age")
        parser.add_argument("occupation")
        args = parser.parse_args()

        for user in users:
            if(name == user["name"]):
                user["age"] = args["age"]
                user["occupation"] = args["occupation"]
                return user, 200

        user = {
            "name": name,
            "age": args["age"],
            "occupation": args["occupation"]
        }
        users.append(user)
        return user, 201

    def delete(self, name):
        global users
        users = [user for user in users if user["name"] != name]
        return "{} is deleted.".format(name), 200
