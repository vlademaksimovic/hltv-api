from flask import abort
from functools import reduce
import logging

logger = logging.getLogger(__name__)

handler = logging.FileHandler('matches_live.log')
handler.setLevel(logging.INFO)

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)

BASE_URL = 'https://www.hltv.org'
MATCHES_URL = BASE_URL + '/matches'


def get(requester, match_filter):
    if match_filter:
        filter_mapping = {
            'live': _filter_live,
        }

        if not filter_mapping[match_filter]:
            abort(400)  # Bad request

        return filter_mapping[match_filter](requester)

    else:  # If no filter
        parsed_content = requester.request(MATCHES_URL)
        upcoming_matches = parsed_content.find_all(
            'div', attrs={'class': 'match-day'})
        live_matches = parsed_content.find_all(
            'div', attrs={'class': 'live-match'})

        if len(upcoming_matches) == 0 or len(live_matches) == 0:
            return None

        # Flatmap to transform [[],[]] to []
        upcoming_matches = reduce(
            list.__add__, list(map(_parse_match_days, upcoming_matches)))
        live_matches = _filter_live(requester, live_matches)
        live_matches = live_matches.get('live')

        return {
            'live': live_matches,
            'upcoming': upcoming_matches,
        }


def _filter_live(requester, live_matches=None):
    if not live_matches:
        parsed_content = requester.request(MATCHES_URL)
        live_matches = parsed_content.find_all(
            'div', attrs={'class': 'live-match'})

    if len(live_matches) == 0:
        return None

    result = list(map(_parse_live_match, live_matches))
    result = list(filter(lambda ele: ele is not None, result))
    return {
        'live': result,
    }


def _parse_live_match(match):
    if 'no-height' in match.attrs['class']:
        # This means an empty div has been generated but it doesn't contain
        # any information yet
        return None

    try:
        _teams = match.select('td.teams span.team-name')
        team1 = _teams[0].get_text()
        team2 = _teams[1].get_text()

        match_type = match.select_one('tr.header > td.bestof').get_text()
        event = match.select_one('div.line-align > div.event-name').get_text()

        _maps = match.select('tr.header > td.map')
        _table_rows = match.select('table tr')

        _score_team1 = _table_rows[1].select('td.mapscore')
        _score_team2 = _table_rows[2].select('td.mapscore')

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


def _parse_map(map, t1_score, t2_score):
    map = map.get_text()
    t1_score = t1_score.get_text()
    t2_score = t2_score.get_text()

    if t1_score != '-':
        t1_score = int(t1_score)

    if t2_score != '-':
        t2_score = int(t2_score)

    return {
        'name': map,
        'team1_score': t1_score,
        'team2_score': t2_score,
    }


def _parse_match_days(day_with_matches):
    try:
        i = 0
        _results = []
        date = _get_text(day_with_matches, 'span.standard-headline')

        for match in _get_tags(day_with_matches, 'a.upcoming-match'):
            _result = {}

            time = _get_text(match, 'td.time')
            time = time.replace('\n', '')

            match_link = BASE_URL + _get_tags(
                day_with_matches,
                'a.upcoming-match')[i].get('href')
            i += 1

            # If placeholder match
            if _get_tag(match, 'td.placeholder-text-cell'):
                _results.append({
                    'date': date,
                    'event': _get_text(match, 'td.placeholder-text-cell'),
                    'match_link': match_link,
                    'time': time,
                })
                continue

            _teams = _get_tags(match, 'td.team-cell')
            team1 = _get_text(_teams[0], 'div.team')
            team2 = _get_text(_teams[1], 'div.team')

            event = _get_text(match, 'td.event > span.event-name')
            map = _get_text(match, 'td.star-cell div.map-text')

            _result.update({
                'date': date,
                'event': event,
                'map': map,
                'match_link': match_link,
                'team1': team1,
                'team2': team2,
                'time': time,
            })

            _results.append(_result)

        return _results

    except Exception:
        logger.error('#### START EXCEPTION ####')
        logger.exception(
            'Unable to parse live match with exception followed by HTML:')
        logger.error(day_with_matches)
        logger.error('#### END EXCEPTION ####')

        abort(500)  # Internal server error


def _get_tag(element, selector):
    return element.select_one(selector)


def _get_tags(element, selector):
    return element.select(selector)


def _get_text(element, selector):
    return _get_tag(element, selector).get_text()
