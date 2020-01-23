from marshmallow import Schema, fields


class ComputedPK:
    pk = fields.Method('get_pk', deserialize='deserialize_pk')

    def get_pk(self, obj):
        return obj.id

    def deserialize_pk(self, value):
        return value


class UserSchema(Schema, ComputedPK):
    name = fields.Str(required=True)
    slug = fields.Str(dump_only=True)


class StreamSchema(Schema, ComputedPK):
    name = fields.Str(required=True)
    slug = fields.Str(dump_only=True)
    description = fields.Str()
    user = fields.Nested('UserSchema', only=['pk', 'slug', 'name'])


class PostSchema(Schema, ComputedPK):
    stream = fields.Nested('StreamSchema', only=['pk', 'slug', 'name'])
    title = fields.Str()
    slug = fields.Str(dump_only=True)
    text = fields.Str(required=True)
    text_html = fields.Str(dump_only=True)
    date = fields.DateTime(format='rfc')


class AccountSchema(Schema):
    name = fields.Str(required=True)
    password = fields.Str(required=True)


user_schema = UserSchema()
stream_schema = StreamSchema()
post_schema = PostSchema()
account_schema = AccountSchema()
