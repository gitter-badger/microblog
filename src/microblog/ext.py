from flask_jwt_extended import JWTManager
from flask_restplus import Api
from pony.flask import Pony

api = Api()
pony = Pony()
jwt = JWTManager()
