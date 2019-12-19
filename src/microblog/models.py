import os
from datetime import datetime

from pony import orm

db = orm.Database()


class Author(db.Entity):
    name = orm.Required(str, 100, unique=True)
    slug = orm.Required(str, 100)
    posts = orm.Set('Post')


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
    provider='sqlite', filename=os.environ.get('DB_FILENAME', ':memory'), create_db=True
)
db.generate_mapping(create_tables=True)
