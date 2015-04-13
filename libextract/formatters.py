"""
    libextract.formatters
    ~~~~~~~~~~~~~~~~~~~~~

    Formats the results of extraction into serializable
    representations, e.g. JSON, text.
"""

from functools import partial
from libextract.xpaths import FILTER_TEXT


UNLIMITED = float('NaN')


def get_text(node):
    """
    Gets the text contained within the children node
    of a given *node*, joined by a space.
    """
    return ' '.join(node.xpath(FILTER_TEXT))


def split_node_attr(node, attr):
    """
    Given a *node*, split the *attr* of the node
    into a list of strings, suitable for id/class
    handling.
    """
    return (node.get(attr) or '').split()


get_node_id = partial(split_node_attr, attr='id')
get_node_class = partial(split_node_attr, attr='class')


def node_json(node, depth=0):
    """
    Given a *node*, serialize it and recursively
    serialize it's children to a given *depth*.
    Note that if the *depth* runs out (goes to 0),
    the children key will be ``None``.
    """
    return {
        'xpath': node.getroottree().getpath(node),
        'class': get_node_class(node),
        'text': node.text,
        'tag': node.tag,
        'id': get_node_id(node),
        'children': (
            [node_json(n, depth-1) for n in node] if depth else None
        ),
    }


def chunks(iterable, size):
    """
    Yield successive chunks of *size* from a
    given *iterable*.
    """
    chunk = []
    for item in iterable:
        chunk.append(item)
        if len(chunk) == size:
            yield chunk
            chunk = []


def get_table_headings(node):
    for elem in node.iter('th'):
        yield ' '.join(elem.text_content().split())


def get_table_data(node):
    for elem in node.iter('td'):
        yield ' '.join(elem.text_content().split())


def table_json(node):
    """
    Given a table *HtmlElement* (ie. <table>), return
    a list of lists, where the first list contains the
    table headings, and the subsequent lists contain table
    rows of data
    """
    headings = list(get_table_headings(node))
    data = get_table_data(node)
    table = [headings]
    table.extend(chunks(data, len(headings)))
    return table
