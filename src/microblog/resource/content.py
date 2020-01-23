from typing import Tuple

from flask import request, url_for
from flask_restful import Resource
from playhouse.flask_utils import get_object_or_404

from ..ext import api
from ..models import Post, Stream, User
from ..schema import post_schema, stream_schema, user_schema
from ..utils.text import slugify


@api.resource('/posts/recent', endpoint='post.collection.recent')
class RecentPostsCollection(Resource):

    def get(self) -> dict:
        recent = Post.select().order_by(Post.date.desc()).limit(10)
        return post_schema.dump(recent, many=True)


@api.resource('/authors', endpoint='author.collection')
class AuthorCollection(Resource):

    def get(self) -> dict:
        page = request.args.get('p', 1, type=int)
        if page < 1:
            page = 1
        users = User.select().order_by(User.name).paginate(page)
        return user_schema.dump(users, many=True)


@api.resource('/author/<slug>', endpoint='author.item')
class AutorItem(Resource):

    def get(self, slug: str) -> dict:
        user = get_object_or_404(User, (User.slug == slug))
        return user_schema.dump(user)


@api.resource('/author/<slug>/streams', endpoint='author.item.streams')
class AuthorStreamCollection(Resource):

    def get(self, slug: str) -> dict:
        user = get_object_or_404(User, (User.slug == slug))
        page = request.args.get('p', 1, type=int)
        if page < 1:
            page = 1
        streams = Stream.select().where(
            Stream.user == user
        ).order_by(Post.date.desc()).paginate(page)
        return stream_schema.dump(streams, many=True)

    def post(self, slug: str) -> Tuple[dict, int, dict]:
        user = get_object_or_404(User, (User.slug == slug))
        data = post_schema.load(request.get_json())
        name = data['name']
        description = data.get('description')
        stream = Stream.create(
            user=user, name=name, slug=slugify(name), description=description,
        )
        headers = {
            'Location': url_for(
                'stream.item', user_slug=user.slug, stream_slug=stream.slug
            )
        }
        return stream_schema.dump(stream), 201, headers


@api.resource('/stream/<author_slug>/<stream_slug>', endpoint='stream.item')
class StreamItem(Resource):

    def get(self, author_slug: str, stream_slug: str) -> dict:
        user = get_object_or_404(User, (User.slug == author_slug))
        stream = get_object_or_404(
            Stream, (Stream.user == user, Stream.slug == stream_slug)
        )
        return stream_schema.dump(stream)
