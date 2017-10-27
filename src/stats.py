from flask import abort
import logging

from src.utils import \
    get_tag, \
    get_text, \
    get_attr, \
    sanity_check_integer, \
    sanity_check_string

logger = logging.getLogger(__name__)

BASE_URL = 'https://www.hltv.org'
STATS_URL = BASE_URL + '/stats'


def get(requester, limit=None, type_=None):
    sanity_check_integer(limit, 'limit')
    sanity_check_string(type_, 'type_')

    if limit is None:
        limit = 0

    if type_:
        if type_ not in ['players', 'teams']:
            abort(400, 'Type [%s] does not exist' % type_)  # Bad request

        html_response = requester.request(STATS_URL)

        return _parse_items(html_response, limit=limit, type_=type_)

    else:  # If no type_
        html_response = requester.request(STATS_URL)

        players = _parse_items(html_response, limit, type_='players')
        teams = _parse_items(html_response, limit, type_='teams')

        if len(players) == 0 or len(teams) == 0:
            abort(502)  # Bad gateway

        return {
            **players,
            **teams,
        }


def _parse_players(html):
    try:
        basic_info = _get_basic_info(html)
        origin = get_attr(get_tag(html, 'img.flag.country'), 'title').lower()
        picture_url = get_attr(get_tag(html, '.playerPicture > img'), 'src')

        return {
            **basic_info,
            'origin': origin,
            'picture_url': picture_url,
        }

    except Exception:
        _raise_exception(html)


def _parse_teams(html):
    try:
        basic_info = _get_basic_info(html)
        picture_url = get_attr(get_tag(html, 'img.img.logo'), 'src')

        return {
            **basic_info,
            'picture_url': picture_url,
        }

    except Exception:
        _raise_exception(html)


def _parse_items(html, limit, type_):
    if type_ == 'players':
        index = 0
        parse_func = _parse_players
    elif type_ == 'teams':
        index = 1
        parse_func = _parse_teams
    else:
        logger.error('Internal type_ [%s] is not supported' % type_)
        abort(500)

    items = html.find_all('div', attrs={'class': 'col'})
    items = items[index]
    items = items.find_all(
        'div', attrs={'class': 'top-x-box'}, limit=int(limit))

    if len(items) == 0:
        abort(502)  # Bad gateway

    items = list(map(parse_func, items))
    items = list(filter(lambda ele: ele is not None, items))

    return {
        type_: items,
    }


def _get_basic_info(html):
    return {
        'name': _get_name(html),
        'maps': _get_maps(html),
        'rating': _get_rating(html),
        'profile_url': _get_profile_url(html),
    }


def _get_maps(html):
    return int(get_text(html, '.average > .bold'))


def _get_name(html):
    return get_text(html, 'a.name')


def _get_profile_url(html):
    return BASE_URL + get_attr(get_tag(html, 'a.name'), 'href')


def _get_rating(html):
    return float(get_text(html, '.rating > .bold'))


def _raise_exception(html):
    logger.error('#### START EXCEPTION ####')
    logger.exception(
        'Unable to parse HTML with exception followed by HTML:')
    logger.error(html)
    logger.error('#### END EXCEPTION ####')

    abort(500)  # Internal server error
