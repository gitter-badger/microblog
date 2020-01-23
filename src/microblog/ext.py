from flask_jwt_extended import JWTManager
from flask_restful import Api
from playhouse.flask_utils import FlaskDB

api = Api()
dbwrapper = FlaskDB()
jwt = JWTManager()
