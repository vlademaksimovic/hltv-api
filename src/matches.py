from flask import abort
import logging

from src.utils import \
    sanity_check_integer, \
    flatmap, \
    get_text, \
    get_tag, \
    get_tags, \
    get_attr

logger = logging.getLogger(__name__)

handler = logging.FileHandler('matches_live.log')
handler.setLevel(logging.INFO)

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)

BASE_URL = 'https://www.hltv.org'
MATCHES_URL = BASE_URL + '/matches'


def get(requester, filter_=None, limit=None):
    sanity_check_integer(limit, 'limit')

    if filter_:
        filter_mapping = {
            'live': _filter_live,
            'upcoming': _filter_upcoming,
        }

        if not filter_mapping[filter_]:
            # Bad request
            abort(400, 'Filter [%s] does not exist' % filter_)

        result = filter_mapping[filter_](requester, limit=limit)

        # Live matches are optional, they are allowed to be missing
        if filter_ != 'live':
            if len(result.get(filter_)) == 0:
                abort(502)  # Bad gateway

        return result

    else:  # If no filter
        html_response = requester.request(MATCHES_URL)

        upcoming_matches = _filter_upcoming(requester, html_response, limit)
        live_matches = _filter_live(requester, html_response, limit)

        # If there are no upcoming matches something is wrong,
        # but live matches are allowed to be missing
        if len(upcoming_matches.get('upcoming')) == 0:
            abort(502)  # Bad gateway

        return {
            **upcoming_matches,
            **live_matches,
        }


def _filter_live(requester, html_response=None, limit=None):
    if not html_response:
        html_response = requester.request(MATCHES_URL)

    if limit is None:
        limit = 0

    live_matches = html_response.find_all(
        'div', attrs={'class': 'live-match'}, limit=int(limit))

    live_matches = list(map(_parse_live_match, live_matches))
    live_matches = list(filter(lambda ele: ele is not None, live_matches))

    return {
        'live': live_matches,
    }


def _parse_live_match(match):
    if 'no-height' in match.attrs['class']:
        # This means an empty div has been generated but it doesn't contain
        # any information yet
        return None

    try:
        _teams = get_tags(match, 'td.teams span.team-name')
        team1 = get_text(_teams[0])
        team2 = get_text(_teams[1])

        match_type = get_text(match, 'tr.header > td.bestof')
        event = get_text(match, 'div.line-align > div.event-name')

        _maps = get_tags(match, 'tr.header > td.map')
        _table_rows = get_tags(match, 'table tr')

        _score_team1 = get_tags(_table_rows[1], 'td.mapscore span')
        _score_team2 = get_tags(_table_rows[2], 'td.mapscore span')

        map_results = list(map(_parse_map, _maps, _score_team1, _score_team2))

        return {
            'team1': team1,
            'team2': team2,
            'event': event,
            'match_type': match_type,
            'maps': map_results,
        }

    except Exception:
        logger.error('#### START EXCEPTION ####')
        logger.exception(
            'Unable to parse live match with exception followed by HTML:')
        logger.error(match)
        logger.error('#### END EXCEPTION ####')

        abort(500)  # Internal server error


def _parse_map(map_, t1_score, t2_score):
    map_ = map_.get_text()
    t1_score = t1_score.get_text()
    t2_score = t2_score.get_text()

    if t1_score != '-':
        t1_score = int(t1_score)

    if t2_score != '-':
        t2_score = int(t2_score)

    return {
        'name': map_,
        'team1_score': t1_score,
        'team2_score': t2_score,
    }


def _filter_upcoming(requester, html_response=None, limit=None):
    if not html_response:
        html_response = requester.request(MATCHES_URL)

    upcoming_matches = html_response.find_all(
        'div', attrs={'class': 'match-day'})

    upcoming_matches = flatmap(
        list(map(_parse_upcoming_matches, upcoming_matches)))

    # TODO: Find an optimized way of limiting the response
    # Idea: in .find_all, pass limit flag as we do in rankings for example
    if limit:
        upcoming_matches = upcoming_matches[:int(limit)]

    return {
        'upcoming': upcoming_matches,
    }


def _parse_upcoming_matches(upcoming_matches):
    try:
        i = 0
        _results = []
        date = get_text(upcoming_matches, 'span.standard-headline')

        for match in get_tags(upcoming_matches, 'a.upcoming-match'):
            _result = {}

            start_time = get_text(match, 'td.time')
            start_time = start_time.replace('\n', '')

            match_url = BASE_URL + get_attr(
                get_tags(
                    upcoming_matches,
                    'a.upcoming-match')[i],
                'href')
            i += 1

            # If placeholder match
            if get_tag(match, 'td.placeholder-text-cell'):
                _results.append({
                    'date': date,
                    'event': get_text(match, 'td.placeholder-text-cell'),
                    'match_url': match_url,
                    'start_time': start_time,
                })
                continue

            _teams = get_tags(match, 'td.team-cell')
            team1 = get_text(_teams[0], 'div.team')
            team2 = get_text(_teams[1], 'div.team')

            event = get_text(match, 'td.event > span.event-name')
            map_ = get_text(match, 'td.star-cell div.map-text')

            _result.update({
                'date': date,
                'event': event,
                'map': map_,
                'match_url': match_url,
                'team1': team1,
                'team2': team2,
                'start_time': start_time,
            })

            _results.append(_result)

        return _results

    except Exception:
        logger.error('#### START EXCEPTION ####')
        logger.exception(
            'Unable to parse live match with exception followed by HTML:')
        logger.error(upcoming_matches)
        logger.error('#### END EXCEPTION ####')

        abort(500)  # Internal server error
