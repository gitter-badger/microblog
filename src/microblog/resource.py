from flask import abort, request
from flask_jwt_extended import (
    create_access_token, create_refresh_token, get_jwt_identity, get_raw_jwt,
    jwt_refresh_token_required, jwt_required,
)
from flask_restful import Resource, reqparse
from passlib.context import CryptContext
from pony import orm

from .models import Author, Post, RevokedToken, db
from .schema import author_schema, post_schema
from .utils.text import slugify

parser = reqparse.RequestParser()
parser.add_argument('name', help='This field can not be blank', required=True)
parser.add_argument('password', help='This field can not be blank', required=True)

pwcontext = CryptContext(schemes=['argon2'])


class RegisterResource(Resource):

    def post(self):
        data = parser.parse_args()
        name = data['name']
        if Author.get(name=name):
            return {'message': f'user {name} already exists'}, 400
        new_user = Author(
            name=name, password=pwcontext.hash(data['password']),
            slug=slugify(data['name']),
        )
        try:
            db.commit()
        except Exception:
            return {'message': 'Something went wrong'}, 500
        else:
            access_token = create_access_token(identity=name)
            refresh_token = create_refresh_token(identity=name)
            return {
                'message': f'user {new_user.name} registered',
                'access_token': access_token,
                'refresh_token': refresh_token,
            }


class UserLogin(Resource):

    def post(self):
        data = parser.parse_args()
        name = data['name']
        user = Author.get(name=name)
        if not user or pwcontext.verify(data['password'], user.password):
            return {'message': f'user {name} does not exist or wrong credentials'}, 400
        return {
            'access_token': create_access_token(identity=name),
            'refresh_token': create_refresh_token(identity=name),
            'message': f'user {name} logged in'
        }


class UserLogoutAccess(Resource):

    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        RevokedToken(jti=jti)
        try:
            db.commit()
        except Exception:
            return {'message': 'something went wrong'}, 500
        else:
            return {'message': 'access token revoked'}


class UserLogoutRefresh(Resource):

    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        RevokedToken(jti=jti)
        try:
            db.commit()
        except Exception:
            return {'message': 'something went wrong'}, 500
        else:
            return {'message': 'refresh token revoked'}


class TokenRefresh(Resource):

    @jwt_refresh_token_required
    def post(self):
        user = get_jwt_identity()
        return {
            'access_token': create_access_token(identity=user)
        }


class HomeResource(Resource):

    def get(self):
        recent = Post.select().order_by(orm.desc(Post.date))[:10]
        return post_schema.dump(recent, many=True)


class PostResource(Resource):

    def on_get(self, author_slug: str, post_slug: str):
        author = Author.get(slug=author_slug)
        if author is None:
            raise abort(404)
        post = Post.get(author=author, slug=post_slug)
        if post is None:
            raise abort(404)
        return post_schema.dump(post)


class AuthorResource(Resource):

    def on_get(self, slug: str):
        author = Author.get(slug=slug)
        if author is None:
            raise abort(404)
        page = request.args.getlist('p', type=int)
        try:
            page = page[0]
        except IndexError:
            page = 1
        posts = orm.select(
            p for p in Post if p.author == author
        ).order_by(orm.desc(Post.date)).page(page)
        return {
            'author': author_schema.dump(author),
            'posts': post_schema.dump(posts, many=True)
        }
