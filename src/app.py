import os
import logging
import re
from flask import Flask, abort, jsonify
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

is_production = bool(os.environ.get('IS_PRODUCTION', default=False))


@app.route('/v1/ranking', methods=['GET'])
def ranking():
    url = 'https://www.hltv.org/ranking/teams'
    parsed_content = _request(url)

    teams = parsed_content.find_all('div', attrs={'class': 'ranked-team'})

    if not teams:
        abort(503)

    return jsonify({'ranking': list(map(_parse_team, teams))})


def _request(url):
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


def _parse_team(team):
    name = team.select_one('span.name').get_text()
    pos = team.select_one('span.position').get_text().replace('#', '')
    points = _get_num(team.select_one('span.points').get_text())
    return {
        'name': name,
        'position': pos,
        'points': points,
    }


def _get_num(string):
    return re.findall('\d+', string)[0]


if __name__ == '__main__':
    app.run(debug=not is_production)
