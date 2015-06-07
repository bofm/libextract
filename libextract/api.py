from functools import partial
from collections import namedtuple

from ._compat import BytesIO
from .core import parse_html, pipeline, select, measure, rank, finalise

Extracted = namedtuple('Extracted', 'nodes, tree')


def extract(document, encoding='utf-8', count=None):
    if isinstance(document, bytes):
        document = BytesIO(document)

    crank = partial(rank, count=count) if count else rank

    tree = parse_html(document, encoding=encoding)
    nodes = pipeline(select(tree), (measure, crank, finalise))

    return Extracted(nodes=nodes, tree=tree)
