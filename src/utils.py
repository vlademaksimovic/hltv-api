from functools import reduce
from flask import abort
import re
import logging

logger = logging.getLogger(__name__)


def sanity_check_integer(param, name):
    """Used for checking URL params inputted by the user"""
    if param is None:
        return

    try:
        param = int(param)
        if param == 0:
            abort(400, 'Parameter %s cannot be 0' % name)  # Bad request

    except TypeError and ValueError:
        logger.exception('Failed to parse %s to integer' % name)
        # Bad request
        abort(400, 'Parameter %s must be integer greater than 0' % name)


def flatmap(input_list):
    """[[a, b], [c, d]] -> [a, b, c, d]"""
    return reduce(list.__add__, input_list)


def get_tag(element, selector):
    return element.select_one(selector)


def get_tags(element, selector):
    return element.select(selector)


def get_text(element, selector):
    return get_tag(element, selector).get_text()


def extract_digits(string):
    return re.findall('\d+', string)[0]
