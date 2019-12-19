import re

from markdown import markdown
from text_unidecode import unidecode

_punctuation_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')


def slugify(text: str, delim: str = '-') -> str:
    result = []
    for word in _punctuation_re.split(text.lower()):
        result.extend(unidecode(word).split())
    return delim.join(result)


def md2html(text: str) -> str:
    return markdown(
        text,
        extensions=[
            'abbr', 'def_list', 'fenced_code', 'footnotes', 'tables', 'nl2br',
            'sane_lists', 'toc',
        ],
    )
