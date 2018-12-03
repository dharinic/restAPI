import os


from flask import Flask , render_template,  request
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_httpauth import HTTPBasicAuth

resttest = Flask(__name__)
api = Api(resttest)
auth = HTTPBasicAuth()

@resttest.route('/',  methods=["GET", "POST"])
def signup():
    if request.form:
        print(request.form)
    return render_template("signup.html")


project_dir = os.path.dirname(os.path.abspath(__file__))

resttest.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resttest.db'
resttest.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
resttest.config['SECRET_KEY'] = 'some-secret-string'

db = ""
db = SQLAlchemy(resttest)


@resttest.before_first_request
def create_tables():
    db.create_all()

resttest.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
jwt = JWTManager(resttest)

import views, models, resources

api.add_resource(resources.User, "/user/<string:name>")
api.add_resource(resources.UserReg, "/registration")
api.add_resource(resources.UserLogin, "/login")
api.add_resource(resources.SecretResource, '/secret')
