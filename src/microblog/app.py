from falcon import API

from .resource import author_resource, home_resource, post_resource


class Microblog(API):

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.add_route('/api/recent', home_resource)
        self.add_route('/api/post/{author_slug}/{post_slug}', post_resource)
        self.add_route('/api/author/{slug}', author_resource)


def create_app():
    return Microblog()


app = application = create_app()
