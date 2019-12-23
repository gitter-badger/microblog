from typing import Tuple

from flask import request, url_for, abort
from flask_restful import Resource

from ..ext import api
from ..models import Author, db
from ..schema import author_schema
from ..utils.text import slugify


@api.resource('/accounts')
class AccountCollection(Resource):

    def get(self) -> dict:
        page = request.args.get('p', 1, type=int)
        if page < 1:
            page = 1
        authors = Author.select().order_by(Author.name).page(page)
        return author_schema.dump(authors, many=True)

    def post(self) -> Tuple[dict, int, dict]:
        data = author_schema.load(request.get_json())
        name = data['name']
        if Author.get(name=name):
            return {'message': f'name {name} already taken'}, 400
        slug = slugify(name)
        author = Author(name=name, slug=slug)
        db.commit()
        headers = {'Location': url_for('account', slug=slug)}
        return author_schema.dump(author), 201, headers


@api.resource('/account/<slug>', endpoint='account')
class AccountItem(Resource):

    def get(self, slug: str) -> dict:
        author = Author.get(slug=slug)
        if author is None:
            abort(404)
        return author_schema.dump(author)
