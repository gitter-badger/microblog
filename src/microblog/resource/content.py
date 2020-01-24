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


@api.resource('/users', endpoint='user.collection')
class UserCollection(Resource):

    def get(self) -> dict:
        page = request.args.get('p', 1, type=int)
        if page < 1:
            page = 1
        users = User.select().order_by(User.name).paginate(page)
        return user_schema.dump(users, many=True)


@api.resource('/user/<int:pk>', endpoint='user.item')
class UserItem(Resource):

    def get(self, pk: int) -> dict:
        user = get_object_or_404(User, (User.id == pk))
        return user_schema.dump(user)


@api.resource('/user/<int:pk>/streams', endpoint='user.item.streams')
class UserStreamCollection(Resource):

    def get(self, pk: int) -> dict:
        user = get_object_or_404(User, (User.id == pk))
        page = request.args.get('p', 1, type=int)
        if page < 1:
            page = 1
        streams = Stream.select().where(
            Stream.user == user
        ).order_by(Stream.name).paginate(page)
        return stream_schema.dump(streams, many=True)

    def post(self, pk: int) -> Tuple[dict, int, dict]:
        user = get_object_or_404(User, (User.id == pk))
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


@api.resource('/user/<int:pk>/posts', endpoint='user.item.posts')
class UserPostCollection(Resource):

    def get(self, pk: int):
        get_object_or_404(User, (User.id == pk))
        page = request.args.get('p', 1, type=int)
        if page < 1:
            page = 1
        posts = Post.select().join(
            Stream, on=(Post.stream == Stream.id)
        ).join(
            User, on=(Stream.user == User.id)
        ).where(
            User.id == pk
        ).order_by(Post.date.desc()).paginate(page)
        return post_schema.dump(posts, many=True)


@api.resource('/stream/<int:pk>', endpoint='stream.item')
class StreamItem(Resource):

    def get(self, pk: int) -> dict:
        stream = get_object_or_404(Stream, (Stream.id == pk))
        return stream_schema.dump(stream)
