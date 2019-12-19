import os
from collections import namedtuple
from datetime import datetime

from pony import orm

db = orm.Database()


PostIdent = namedtuple('PostIdent', ['a_slug', 'p_slug'])


class Author(db.Entity):
    name = orm.Required(str, 100, unique=True)
    slug = orm.Required(str, 100)
    posts = orm.Set('Post')

    @property
    def post_idents(self):
        return [p.ident for p in self.posts.order_by(orm.desc(Post.date))]


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

    @property
    def ident(self):
        return PostIdent(self.author.slug, self.slug)._asdict()


db.bind(
    provider='sqlite', filename=os.environ.get('DB_FILENAME', ':memory:'),
    create_db=True,
)
db.generate_mapping(create_tables=True)
