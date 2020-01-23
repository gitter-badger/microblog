from datetime import datetime, timedelta
from typing import Optional, Tuple

from flask import Response, jsonify, request, url_for
from flask_jwt_extended import (
    create_access_token, create_refresh_token, get_jwt_identity, get_raw_jwt,
    jwt_refresh_token_required, jwt_required,
)
from flask_restful import Resource
from marshmallow import ValidationError
from playhouse.flask_utils import get_object_or_404

from ..ext import api
from ..models import RevokedToken, User, db
from ..schema import account_schema, user_schema
from ..utils.text import slugify

REFRESH_TOKEN_MAX_AGE = 60 * 60 * 24 * 365 * 4  # roughly 4 years


def authentication_response(
            user: User, code: int = 200, headers: Optional[dict] = None
        ) -> Response:
    data = user_schema.dump(user)
    data['access_token'] = create_access_token(user.id)
    resp = jsonify(data)
    resp.status_code = code
    if headers:
        resp.headers.extend(headers)
    cookie_expiry = datetime.utcnow() + timedelta(seconds=REFRESH_TOKEN_MAX_AGE)
    resp.set_cookie(
        'refresh_token', value=create_refresh_token(user.id),
        max_age=REFRESH_TOKEN_MAX_AGE, expires=cookie_expiry, httponly=True,
        samesite='Strict',
    )
    return resp


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
        with db.atomic():
            user.save()
            headers = {'Location': url_for('account.item', slug=slug)}
            return authentication_response(user, 201, headers)


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
        return authentication_response(user)


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
        resp = jsonify({'message': 'Refresh token revoked'})
        resp.delete_cookie('refresh_token')
        return resp


@api.resource('/token/refresh', endpoint='account.tokenrefresh')
class TokenRefresh(Resource):

    @jwt_refresh_token_required
    def post(self) -> dict:
        return {'access_token': create_access_token(get_jwt_identity())}
