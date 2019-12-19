from falcon import Request, Response
from pony import orm

from .models import Post
from .schema import post_schema


class HomeResource:

    @orm.db_session
    def on_get(self, req: Request, resp: Response):
        recent = Post.select().order_by(orm.desc(Post.date))[:10]
        resp.body = post_schema.dumps(recent, many=True)


home_resource = HomeResource()
