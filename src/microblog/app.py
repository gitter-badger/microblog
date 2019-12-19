from falcon import API


class Microblog(API):
    pass


def create_app():
    return Microblog()


app = application = Microblog()
