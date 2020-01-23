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
from ..models import Author, RevokedToken
from ..schema import account_schema, author_schema
from ..utils.text import slugify


@api.resource('/accounts', endpoint='account.collection')
class AccountCollection(Resource):

    def get(self) -> dict:
        page = request.args.get('p', 1, type=int)
        if page < 1:
            page = 1
        authors = Author.select().order_by(Author.name).paginate(page)
        return author_schema.dump(authors, many=True)

    def post(self) -> Tuple[dict, int, dict]:
        try:
            data = account_schema.load(request.get_json())
        except ValidationError as e:
            return {'errors': e.messages}, 400
        name = data['name']
        if Author.get_or_none(Author.name == name):
            return {'message': f'name {name} already taken'}, 400
        slug = slugify(name)
        author = Author(name=name, slug=slug)
        author.set_password(data['password'])
        author.save()
        headers = {'Location': url_for('account.item', slug=slug)}
        rv = author_schema.dump(author)
        rv['access_token'] = create_access_token(author.id)
        rv['refresh_token'] = create_refresh_token(author.id)
        return rv, 201, headers


@api.resource('/account/<slug>', endpoint='account.item')
class AccountItem(Resource):

    def get(self, slug: str) -> dict:
        author = get_object_or_404(Author, (Author.slug == slug))
        return author_schema.dump(author)


@api.resource('/login', endpoint='account.login')
class Login(Resource):

    def post(self) -> dict:
        try:
            data = account_schema.load(request.get_json())
        except ValidationError as e:
            return {'errors': e.messages}, 400
        author = Author.get_or_none(Author.name == data['name'])
        if not author or not author.check_password(data['password']):
            return {'error': 'no account with that credentials'}, 400
        rv = author_schema.dump(author)
        rv['access_token'] = create_access_token(author.id)
        rv['refresh_token'] = create_refresh_token(author.id)
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
