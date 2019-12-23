import os
from datetime import datetime

from pony import orm

from .sec import pw_context

db = orm.Database()


class Author(db.Entity):
    name = orm.Required(str, 120, unique=True)
    password = orm.Required(str, 120)
    slug = orm.Required(str, 120)
    posts = orm.Set('Post')

    def check_password(self, password):
        return pw_context.verify(password, self.password)


class RevokedToken(db.Entity):
    jti = orm.Required(str, 120)

    @classmethod
    def is_blacklisted(cls, jti: str) -> bool:
        return cls.get(jti=jti) is not None


class Post(db.Entity):
    author = orm.Required(Author)
    title = orm.Required(str, 200)
    slug = orm.Required(str, 200)
    text = orm.Required(str)
    text_html = orm.Optional(str)
    date = orm.Required(datetime, default=datetime.utcnow)
    year = orm.Optional(int)
    month = orm.Optional(int)
    day = orm.Optional(int)
    orm.composite_index(year, month)
    orm.composite_key(author, slug)


db.bind(
    provider='sqlite', filename=os.environ.get('DB_FILENAME', ':memory:'),
    create_db=True,
)
db.generate_mapping(create_tables=True)
