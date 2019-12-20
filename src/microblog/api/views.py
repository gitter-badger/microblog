from datetime import datetime

from flask import Response, abort, jsonify, request, url_for
from pony import orm

from ..models import Author, Post, db
from ..schema import author_schema, post_schema
from ..utils.text import md2html, slugify
from . import api_bp


@api_bp.route('/recent')
def recent() -> Response:
    recent = Post.select().order_by(orm.desc(Post.date))[:10]
    return jsonify(post_schema.dump(recent, many=True))


@api_bp.route('/authors/register', methods=['POST'])
def register() -> Response:
    data = author_schema.load(request.get_json())
    name = data['name']
    if Author.get(name=name):
        return jsonify({'message': f'name {name} already taken'}), 400
    slug = slugify(name)
    author = Author(name=name, slug=slug)
    db.commit()
    resp = jsonify({
        'message': f'author {author.name} created'
    })
    resp.headers['Location'] = url_for('api.author', slug=slug)
    resp.status_code = 201
    return resp


@api_bp.route('/author/<slug>')
def author(slug: str) -> Response:
    author = Author.get(slug=slug)
    if author is None:
        abort(404)
    return jsonify(author_schema.dump(author))


@api_bp.route('/author/<slug>/posts', methods=['POST', 'GET'])
def author_posts(slug: str) -> Response:
    if request.method == 'POST':
        author = Author.get(slug=slug)
        if author is None:
            abort(404)
        data = post_schema.load(request.get_json())
        post_date = data.get('date') or datetime.utcnow()
        year, month, day = post_date.year, post_date.month, post_date.day
        title = data['title']
        text = data['text']
        post = Post(
            author=author, title=title, slug=slugify(title),
            text=text, text_html=md2html(text),
            date=post_date, year=year, month=month, day=day,
        )
        db.commit()
        resp = jsonify(post_schema.dump(post))
        resp.status_code = 201
        resp.headers['Location'] = url_for(
            'api.post', author_slug=author.slug, post_slug=post.slug
        )
        return resp
    author = Author.get(slug=slug)
    if author is None:
        abort(404)
    page = request.args.get('p', 1, type=int)
    if page < 1:
        page = 1
    posts = Post.select(lambda p: p.author == author).order_by(orm.desc(Post.date))
    return jsonify(post_schema.dump(posts, many=True))


@api_bp.route('/post/<author_slug>/<post_slug>')
def post(author_slug: str, post_slug: str) -> Response:
    author = Author.get(slug=author_slug)
    if author is None:
        abort(404)
    post = Post.get(author=author, slug=post_slug)
    if post is None:
        abort(404)
    return jsonify(post_schema.dump(post))
