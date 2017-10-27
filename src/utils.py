from functools import reduce

import datetime
from flask import abort
import re
import logging

logger = logging.getLogger(__name__)


def sanity_check_integer(param, name):
    """Sanity check user inputted URL param of type integer"""
    if param is None:
        return

    try:
        param = int(param)
        if param == 0:
            abort(400, 'Parameter [%i] cannot be 0' % name)  # Bad request

    except TypeError and ValueError:
        logger.exception('Failed to parse [%s] to integer' % name)
        # Bad request
        abort(400, 'Parameter [%s] must be integer greater than 0' % name)


def sanity_check_string(param, name):
    """Sanity check user inputted URL param of type string"""
    if param is None:
        return

    try:
        param = str(param)
        if param == '':
            abort(400, 'Parameter [%s] cannot be empty' % name)  # Bad request

    except TypeError and ValueError:
        logger.exception('Failed to parse [%i] to string' % name)
        # Bad request
        abort(400,
              'Parameter [%i] must be string with at least 1 character' % name)


def flatmap(input_list):
    """[[a, b], [c, d]] -> [a, b, c, d]"""
    if not input_list:
        return input_list
    return reduce(list.__add__, input_list)


def get_tag(element, selector):
    return element.select_one(selector)


def get_tags(element, selector):
    return element.select(selector)


def get_text(element, selector=None):
    if selector is None:
        return element.get_text()
    return get_tag(element, selector).get_text()


def get_attr(element, attribute):
    return element.get(attribute)


def extract_digits(string):
    return re.findall('\d+', string)[0]


def get_count(list_or_none):
    """Returns length of list if list exist, otherwise return 0"""
    return len(list_or_none) if list_or_none else 0


def get_milliseconds_delta(start, end):
    if not isinstance(start, datetime.datetime) or \
            not isinstance(end, datetime.datetime):
        raise TypeError

    return (end - start).microseconds / 1000
