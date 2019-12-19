from falcon import API

from .resource import home_resource


class Microblog(API):

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.add_route('/recent', home_resource)


def create_app():
    return Microblog()


app = application = create_app()
