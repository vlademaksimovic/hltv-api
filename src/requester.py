import json
import logging
from random import randint
from flask import abort
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def request(url):
    if not url:
        logger.error('Missing URL argument')
        abort(500)  # Internal server error

    req = Request(url, headers={'User-Agent': _get_random_user_agent()})
    conn = urlopen(req)
    parsed_content = BeautifulSoup(conn.read(), 'html.parser')

    if not parsed_content:
        logger.error('Response is empty')
        abort(502)  # Bad gateway

    return parsed_content


def _get_random_user_agent():
    # This will hopefully decrease the risk of getting blacklisted
    with open('src/resources/user_agents.json', encoding='utf-8') as file:
        user_agents = json.load(file)
        count = len(user_agents)
        random_int = randint(0, (count - 1))
        return user_agents[random_int]
