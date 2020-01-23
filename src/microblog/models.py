from datetime import datetime

from peewee import CharField, DateTimeField, ForeignKeyField, IntegerField, TextField
from werkzeug.security import check_password_hash, generate_password_hash

from .ext import dbwrapper


class Author(dbwrapper.Model):
    name = CharField(max_length=120, unique=True, null=False)
    password = TextField(null=False)
    slug = CharField(max_length=120, null=False)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_password(self, password):
        self.password = generate_password_hash(password)


class RevokedToken(dbwrapper.Model):
    jti = CharField(max_length=120, null=False, index=True)

    @classmethod
    def is_blacklisted(cls, jti: str) -> bool:
        return cls.get_or_none(cls.jti == jti) is not None


class Post(dbwrapper.Model):
    author = ForeignKeyField(Author, backref='posts', null=False)
    title = CharField(max_length=200, null=False)
    slug = CharField(max_length=200, null=False)
    text = TextField(null=False)
    text_html = TextField(null=True)
    date = DateTimeField(null=False, default=datetime.utcnow)
    year = IntegerField(null=True)
    month = IntegerField(null=True)
    day = IntegerField(null=True)

    class Meta:
        indexes = (
            (('year', 'month', 'day', 'slug', 'author'), True),
        )
