from flask import abort, request
from flask_jwt_extended import (
    create_access_token, create_refresh_token, get_jwt_identity, get_raw_jwt,
    jwt_refresh_token_required, jwt_required,
)
from flask_restplus import Resource, reqparse
from passlib.context import CryptContext
from pony import orm

from .ext import api
from .models import Author, Post, RevokedToken, db
from .schema import author_schema, post_schema
from .utils.text import slugify

parser = reqparse.RequestParser()
parser.add_argument('name', help='This field can not be blank', required=True)
parser.add_argument('password', help='This field can not be blank', required=True)

pwcontext = CryptContext(schemes=['argon2'])


@api.route('/register')
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


@api.route('/login')
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


@api.route('/logout/access')
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


@api.route('/logout/refresh')
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


@api.route('/token/refresh')
class TokenRefresh(Resource):

    @jwt_refresh_token_required
    def post(self):
        user = get_jwt_identity()
        return {
            'access_token': create_access_token(identity=user)
        }


@api.route('/users')
class AllUsers(Resource):

    def get(self):
        authors = Author.select()
        return author_schema.dump(authors, many=True)

    def delete(self):
        Author.select().delete()
        return {'message': 'all authors deleted'}


@api.route('/secret')
class SecretResource(Resource):

    @jwt_required
    def get(self):
        return {
            'answer': 42
        }


@api.route('/recent')
class HomeResource(Resource):

    def get(self):
        recent = Post.select().order_by(orm.desc(Post.date))[:10]
        return post_schema.dump(recent, many=True)


@api.route('/post/<string:author_slug>/<string:post_slug>')
class PostResource(Resource):

    def on_get(self, author_slug: str, post_slug: str):
        author = Author.get(slug=author_slug)
        if author is None:
            raise abort(404)
        post = Post.get(author=author, slug=post_slug)
        if post is None:
            raise abort(404)
        return post_schema.dump(post)


@api.route('/author/<string:slug>')
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
