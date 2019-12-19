from marshmallow import Schema, fields


class ComputedPK:
    pk = fields.Method('get_pk', deserialize='deserialize_pk')

    def get_pk(self, obj):
        return obj.id

    def deserialize_pk(self, value):
        return value


class AuthorSchema(Schema, ComputedPK):
    name = fields.Str(required=True)
    slug = fields.Str(dump_only=True)
    post_idents = fields.Nested(
        'PostIdentSchema', many=True, dump_only=True, data_key='posts'
    )


class PostSchema(Schema, ComputedPK):
    author = fields.Nested('AuthorSchema', only=['pk', 'slug', 'name'])
    title = fields.Str(required=True)
    slug = fields.Str(dump_only=True)
    text = fields.Str(required=True)
    text_html = fields.Str(dump_only=True)
    date = fields.DateTime(format='rfc')


class PostIdentSchema(Schema):
    a_slug = fields.Str(required=True)
    p_slug = fields.Str(required=True)


author_schema = AuthorSchema()
post_schema = PostSchema()
