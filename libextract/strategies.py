from __future__ import absolute_import

# TODO: circular dependencies?
from libextract.html.tabular import STRATEGY as TABULAR
from libextract.html.article import STRATEGY, get_text

ARTICLE_NODE = STRATEGY
ARTICLE_TEXT = ARTICLE_NODE + (get_text,)
