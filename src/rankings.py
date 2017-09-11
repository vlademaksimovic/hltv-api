from flask import abort
import re
import logging

logger = logging.getLogger(__name__)

URL = 'https://www.hltv.org/ranking/teams'


def get(requester, limit=None):
    _sanity_check(limit)

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


def _sanity_check(limit):
    if limit is None:
        return

    try:
        limit = int(limit)

        if limit == 0:
            abort(400, 'Limit parameter cannot be 0')  # Bad request

    except TypeError and ValueError:
        logger.exception('Unable to parse %s to integer' % str(limit))
        # Bad request
        abort(400, 'Limit parameter must be integer greater than 0')


def _extract_digits(string):
    return re.findall('\d+', string)[0]
