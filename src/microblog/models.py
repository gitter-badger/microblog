from datetime import datetime

from peewee import (
    CharField, DateTimeField, ForeignKeyField, IntegerField, Model, SqliteDatabase,
    TextField, TimeField,
)
from werkzeug.security import check_password_hash, generate_password_hash

db = SqliteDatabase(None)


class User(Model):
    name = CharField(max_length=120, unique=True, null=False)
    password = TextField(null=False)
    slug = CharField(max_length=120, null=False)

    class Meta:
        database = db

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    def set_password(self, password: str):
        self.password = generate_password_hash(password)


class Stream(Model):
    name = CharField(max_length=120, null=False, index=True)
    slug = CharField(max_length=120, null=False, index=True)
    user = ForeignKeyField(User, backref='streams', null=False)
    description = TextField(null=True)

    class Meta:
        database = db
        indexes = (
            (('user', 'slug'), True),
        )


class Post(Model):
    stream = ForeignKeyField(Stream, backref='posts', null=False)
    title = CharField(max_length=200, null=True)
    slug = CharField(max_length=200, null=True)
    text = TextField(null=False)
    text_html = TextField(null=True)
    date = DateTimeField(null=False, default=datetime.utcnow)
    year = IntegerField(null=True)
    month = IntegerField(null=True)
    day = IntegerField(null=True)
    time = TimeField(null=True)

    class Meta:
        database = db
        indexes = (
            (('year', 'month', 'day', 'time', 'stream'), False),
        )


class RevokedToken(Model):
    jti = CharField(max_length=120, null=False, index=True)

    class Meta:
        database = db

    @classmethod
    def is_blacklisted(cls, jti: str) -> bool:
        return cls.get_or_none(cls.jti == jti) is not None
