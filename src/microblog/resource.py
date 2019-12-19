import json

import falcon
from falcon import Request, Response
from pony import orm

from .models import Author, Post
from .schema import author_schema, post_schema


class HomeResource:

    @orm.db_session
    def on_get(self, req: Request, resp: Response):
        recent = Post.select().order_by(orm.desc(Post.date))[:10]
        resp.body = post_schema.dumps(recent, many=True)


home_resource = HomeResource()


class PostResource:

    @orm.db_session
    def on_get(self, req: Request, resp: Response, author_slug: str, post_slug: str):
        author = Author.get(slug=author_slug)
        if author is None:
            raise falcon.HTTPNotFound()
        post = Post.get(author=author, slug=post_slug)
        if post is None:
            raise falcon.HTTPNotFound()
        resp.body = post_schema.dumps(post)


post_resource = PostResource()


class AuthorResource:

    @orm.db_session
    def on_get(self, req: Request, resp: Response, slug: str):
        author = Author.get(slug=slug)
        if author is None:
            raise falcon.HTTPNotFound()
        page = req.params.get('p', '1')
        if not isinstance(page, str):
            page = page[0]
        try:
            page = int(page)
            if page < 1:
                page = 1
        except ValueError:
            raise falcon.HTTPBadRequest()
        posts = orm.select(
            p for p in Post if p.author == author
        ).order_by(orm.desc(Post.date)).page(page)
        rv = {
            'author': author_schema.dump(author),
            'posts': post_schema.dump(posts, many=True)
        }
        resp.body = json.dumps(rv)


author_resource = AuthorResource()
