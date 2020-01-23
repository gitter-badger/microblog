from typing import Tuple

from flask import request, url_for
from flask_jwt_extended import (
    create_access_token, create_refresh_token, get_jwt_identity, get_raw_jwt,
    jwt_refresh_token_required, jwt_required,
)
from flask_restful import Resource
from marshmallow import ValidationError
from playhouse.flask_utils import get_object_or_404

from ..ext import api
from ..models import RevokedToken, User
from ..schema import account_schema, user_schema
from ..utils.text import slugify


@api.resource('/accounts', endpoint='account.collection')
class AccountCollection(Resource):

    def get(self) -> dict:
        page = request.args.get('p', 1, type=int)
        if page < 1:
            page = 1
        users = User.select().order_by(User.name).paginate(page)
        return user_schema.dump(users, many=True)

    def post(self) -> Tuple[dict, int, dict]:
        try:
            data = account_schema.load(request.get_json())
        except ValidationError as e:
            return {'errors': e.messages}, 400
        name = data['name']
        if User.get_or_none(User.name == name):
            return {'message': f'name {name} already taken'}, 400
        slug = slugify(name)
        user = User(name=name, slug=slug)
        user.set_password(data['password'])
        user.save()
        headers = {'Location': url_for('account.item', slug=slug)}
        rv = user_schema.dump(user)
        rv['access_token'] = create_access_token(user.id)
        rv['refresh_token'] = create_refresh_token(user.id)
        return rv, 201, headers


@api.resource('/account/<slug>', endpoint='account.item')
class AccountItem(Resource):

    def get(self, slug: str) -> dict:
        user = get_object_or_404(User, (User.slug == slug))
        return user_schema.dump(user)


@api.resource('/login', endpoint='account.login')
class Login(Resource):

    def post(self) -> dict:
        try:
            data = account_schema.load(request.get_json())
        except ValidationError as e:
            return {'errors': e.messages}, 400
        user = User.get_or_none(User.name == data['name'])
        if not user or not user.check_password(data['password']):
            return {'error': 'no account with that credentials'}, 400
        rv = user_schema.dump(user)
        rv['access_token'] = create_access_token(user.id)
        rv['refresh_token'] = create_refresh_token(user.id)
        return rv


@api.resource('/logout/access', endpoint='account.logout.access')
class LogoutAccess(Resource):

    @jwt_required
    def post(self) -> dict:
        jti = get_raw_jwt()['jti']
        RevokedToken.create(jti=jti)
        return {'message': 'Access token revoked'}


@api.resource('/logout/refresh', endpoint='account.logout.refresh')
class LogoutRefresh(Resource):

    @jwt_refresh_token_required
    def post(self) -> dict:
        jti = get_raw_jwt()['jti']
        RevokedToken.create(jti=jti)
        return {'message': 'Refresh token revoked'}


@api.resource('/token/refresh', endpoint='account.tokenrefresh')
class TokenRefresh(Resource):

    @jwt_refresh_token_required
    def post(self) -> dict:
        return {'access_token': create_access_token(get_jwt_identity())}
