from flask import abort
import logging

logger = logging.getLogger(__name__)

handler = logging.FileHandler('matches_live.log')
handler.setLevel(logging.INFO)

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)

URL = 'https://www.hltv.org/matches'


def get(requester, match_filter):
    if match_filter:
        filter_mapping = {
            'live': _filter_live,
        }

        if not filter_mapping[match_filter]:
            abort(400)  # Bad request

        return filter_mapping[match_filter](requester)

    else:  # If no filter
        # parsed_content = requester.request(URL)
        # all_live_matches = parsed_content.find_all(
        #     'div', attrs={'class': 'live-matches'})
        pass


def _filter_live(requester):
    parsed_content = requester.request(URL)
    all_live_matches = parsed_content.find_all(
        'div', attrs={'class': 'live-match'})

    result = list(map(_parse_live_match, all_live_matches))
    result = list(filter(lambda ele: ele is not None, result))
    return result


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
        logger.exception('#### START EXCEPTION ####')
        logger.exception(
            'Unable to parse live match with exception followed by HTML:')
        logger.exception(match)
        logger.exception('#### END EXCEPTION ####')
        pass


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


def _parse_matches(match):
    pass
