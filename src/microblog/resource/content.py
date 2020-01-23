from datetime import datetime
from typing import Tuple

from flask import request, url_for
from flask_restful import Resource, abort
from playhouse.flask_utils import get_object_or_404

from ..ext import api
from ..models import Author, Post
from ..schema import author_schema, post_schema
from ..utils.text import md2html, slugify


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
        authors = Author.select().order_by(Author.name).paginate(page)
        return author_schema.dump(authors, many=True)


@api.resource('/author/<slug>', endpoint='author.item')
class AutorItem(Resource):

    def get(self, slug: str) -> dict:
        author = get_object_or_404(Author, (Author.slug == slug))
        return author_schema.dump(author)


@api.resource('/author/<slug>/posts', endpoint='author.item.posts')
class AuthorPostCollection(Resource):

    def get(self, slug: str) -> dict:
        author = get_object_or_404(Author, (Author.slug == slug))
        page = request.args.get('p', 1, type=int)
        if page < 1:
            page = 1
        posts = Post.select().where(
            Post.author == author
        ).order_by(Post.date.desc()).paginate(page)
        return post_schema.dump(posts, many=True)

    def post(self, slug: str) -> Tuple[dict, int, dict]:
        author = get_object_or_404(Author, (Author.slug == slug))
        data = post_schema.load(request.get_json())
        post_date = data.get('date') or datetime.utcnow()
        year, month, day = post_date.year, post_date.month, post_date.day
        title = data['title']
        text = data['text']
        post = Post.create(
            author=author, title=title, slug=slugify(title),
            text=text, text_html=md2html(text),
            date=post_date, year=year, month=month, day=day,
        )
        headers = {
            'Location': url_for(
                'post.item', author_slug=author.slug, post_slug=post.slug
            )
        }
        return post_schema.dump(post), 201, headers


@api.resource('/post/<author_slug>/<post_slug>', endpoint='post.item')
class PostItem(Resource):

    def get(self, author_slug: str, post_slug: str) -> dict:
        author = get_object_or_404(Author, (Author.slug == author_slug))
        if author is None:
            abort(404)
        post = Post.get_or_none(Post.author == author, Post.slug == post_slug)
        if post is None:
            abort(404)
        return post_schema.dump(post)
