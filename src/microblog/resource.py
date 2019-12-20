from flask import abort, request
from flask_restful import Resource
from pony import orm

from .models import Author, Post, db
from .schema import author_schema, post_schema
from .utils.text import slugify


class Register(Resource):

    def post(self):
        data = author_schema.load(request.get_json())
        name = data['name']
        if Author.get(name=name):
            return {'message': f'name {name} already taken'}, 400
        slug = slugify(name)
        author = Author(name=name, slug=slug)
        db.commit()
        return {'message': f'author {author.name} created'}, 201


class HomeResource(Resource):

    def get(self):
        recent = Post.select().order_by(orm.desc(Post.date))[:10]
        return post_schema.dump(recent, many=True)


class PostResource(Resource):

    def get(self, author_slug: str, post_slug: str):
        author = Author.get(slug=author_slug)
        if author is None:
            raise abort(404)
        post = Post.get(author=author, slug=post_slug)
        if post is None:
            raise abort(404)
        return post_schema.dump(post)


class AuthorResource(Resource):

    def get(self, slug: str):
        author = Author.get(slug=slug)
        if author is None:
            raise abort(404)
        return author_schema.dump(author)
