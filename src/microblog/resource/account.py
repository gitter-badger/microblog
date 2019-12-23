from typing import Tuple

from flask import abort, request, url_for
from flask_jwt_extended import (
    create_access_token, create_refresh_token, get_jwt_identity, get_raw_jwt,
    jwt_refresh_token_required, jwt_required,
)
from flask_restful import Resource
from marshmallow import ValidationError

from ..ext import api
from ..models import Author, db, RevokedToken
from ..schema import account_schema, author_schema
from ..sec import pw_context
from ..utils.text import slugify


@api.resource('/accounts', endpoint='account.collection')
class AccountCollection(Resource):

    def get(self) -> dict:
        page = request.args.get('p', 1, type=int)
        if page < 1:
            page = 1
        authors = Author.select().order_by(Author.name).page(page)
        return author_schema.dump(authors, many=True)

    def post(self) -> Tuple[dict, int, dict]:
        try:
            data = account_schema.load(request.get_json())
        except ValidationError as e:
            return {'errors': e.messages}, 400
        name = data['name']
        if Author.get(name=name):
            return {'message': f'name {name} already taken'}, 400
        slug = slugify(name)
        pw_hash = pw_context.hash(data['password'])
        author = Author(name=name, password=pw_hash, slug=slug)
        db.commit()
        headers = {'Location': url_for('account.item', slug=slug)}
        rv = author_schema.dump(author)
        rv['access_token'] = create_access_token(author.id)
        rv['refresh_token'] = create_refresh_token(author.id)
        return rv, 201, headers


@api.resource('/account/<slug>', endpoint='account.item')
class AccountItem(Resource):

    def get(self, slug: str) -> dict:
        author = Author.get(slug=slug)
        if author is None:
            abort(404)
        return author_schema.dump(author)


@api.resource('/login', endpoint='account.login')
class Login(Resource):

    def post(self):
        try:
            data = account_schema.load(request.get_json())
        except ValidationError as e:
            return {'errors': e.messages}, 400
        author = Author.get(name=data['name'])
        if not author or not author.check_password(data['password']):
            return {'error': 'no account with that credentials'}, 400
        rv = author_schema.dump(author)
        rv['access_token'] = create_access_token(author.id)
        rv['refresh_token'] = create_refresh_token(author.id)
        return rv


@api.resource('/logout/access', endpoint='account.logout.access')
class LogoutAccess(Resource):

    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        RevokedToken(jti=jti)
        db.commit()
        return {'message': 'Access token revoked'}


@api.resource('/logout/refresh', endpoint='account.logout.refresh')
class LogoutRefresh(Resource):

    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        RevokedToken(jti=jti)
        db.commit()
        return {'message': 'Refresh token revoked'}


@api.resource('/token/refresh', endpoint='account.tokenrefresh')
class TokenRefresh(Resource):

    @jwt_refresh_token_required
    def post(self):
        return {'access_token': create_access_token(get_jwt_identity())}
