import falcon
from falcon import Request, Response
from pony import orm

from .models import Post, Author
from .schema import post_schema


class HomeResource:

    @orm.db_session
    def on_get(self, req: Request, resp: Response):
        recent = Post.select().order_by(orm.desc(Post.date))[:10]
        resp.body = post_schema.dumps(recent, many=True)


home_resource = HomeResource()


class PostResource:

    @orm.db_session
    def on_get(self, req: Request, resp: Response, author_slug, post_slug):
        author = Author.get(slug=author_slug)
        if author is None:
            raise falcon.HTTPNotFound()
        post = Post.get(author=author, slug=post_slug)
        if post is None:
            raise falcon.HTTPNotFound()
        resp.body = post_schema.dumps(post)


post_resource = PostResource()
