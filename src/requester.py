import logging
from flask import abort
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def request(url):
    if not url:
        logger.error('Missing URL argument')
        abort(500)

    # TODO: Randomize headers
    req = Request(url, headers={'User-Agent': 'Magic Browser'})
    conn = urlopen(req)
    parsed_content = BeautifulSoup(conn.read(), 'html.parser')

    if not parsed_content:
        logger.error('Response is empty')
        abort(503)

    return parsed_content
