from flask import abort
import re
import logging

from src.utils import sanity_check_integer

logger = logging.getLogger(__name__)

URL = 'https://www.hltv.org/ranking/teams'


def get(requester, limit=None):
    sanity_check_integer(limit, 'limit')

    if limit is None:
        limit = 0

    parsed_content = requester.request(URL)
    teams = parsed_content.find_all(
        'div', attrs={'class': 'ranked-team'}, limit=int(limit))

    if len(teams) == 0:
        return None

    return list(map(_parse_team, teams))


def _parse_team(team):
    try:
        name = team.select_one('span.name').get_text()
        pos = team.select_one('span.position').get_text().replace('#', '')
        points = _extract_digits(team.select_one('span.points').get_text())

        return {
            'name': name,
            'position': int(pos),
            'points': int(points),
        }

    except Exception:
        logger.error('#### START EXCEPTION ####')
        logger.exception(
            'Unable to parse live match with exception followed by HTML:')
        logger.error(team)
        logger.error('#### END EXCEPTION ####')

        abort(500)  # Internal server error


def _extract_digits(string):
    return re.findall('\d+', string)[0]
