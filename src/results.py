from functools import reduce
from flask import abort
import logging

logger = logging.getLogger(__name__)

BASE_URL = 'https://www.hltv.org'
RESULTS_URL = BASE_URL + '/results'


def get(requester, limit=None, offset=None):
    _sanity_check(limit, 'limit')
    _sanity_check(offset, 'offset')

    url = '%s?offset=%s' % (RESULTS_URL, str(offset)) if offset \
        else RESULTS_URL

    parsed_content = requester.request(url)
    all_days_results = parsed_content.find_all(
        'div', attrs={'class': 'results-sublist'})

    if len(all_days_results) == 0:
        abort(502)  # Bad gateway

    results = _flatmap(list(map(_parse_results, all_days_results)))

    # TODO: Find an optimized way of limiting the response
    if limit:
        results = results[:int(limit)]

    return results


def _parse_results(single_day_results):
    try:
        _results = []
        date = single_day_results.select_one('span.standard-headline')
        date = date.get_text().replace('Results for ', '')

        for match in single_day_results.select('div.result-con'):
            _result = {}

            team1 = _get_text(match, 'div.team1 .team')
            team2 = _get_text(match, 'div.team2 .team')
            event = _get_text(match, 'td.event > span.event-name')
            map = _get_text(match, 'td.star-cell div.map-text')
            match_url = BASE_URL + _get_tag(match, 'a.a-reset').get('href')

            _result.update({
                'date': date,
                'event': event,
                'map': map,
                'match_url': match_url,
                'team1': team1,
                'team2': team2,
            })

            # Result was a tie
            score_tie = _get_tag(match, 'td.result-score > .score-tie')
            if score_tie:
                # Since it was a tie we know that the results are the same
                score = score_tie.get_text()

                _result.update({
                    'score_lost': int(score),
                    'score_won': int(score),
                    'result': 'tie',
                })
            else:
                winner = _get_text(match, 'div.team.team-won')
                score_won = _get_text(
                    match, 'td.result-score > span.score-won')
                score_lost = _get_text(
                    match, 'td.result-score > span.score-lost')

                _result.update({
                    'score_lost': int(score_lost),
                    'score_won': int(score_won),
                    'winner': winner,
                })

            _results.append(_result)

        return _results

    except Exception:
        logger.error('#### START EXCEPTION ####')
        logger.exception(
            'Unable to parse result with exception followed by HTML:')
        logger.error(single_day_results)
        logger.error('#### END EXCEPTION ####')

        abort(500)  # Internal server error


def _sanity_check(param, name):
    if param is None:
        return

    try:
        param = int(param)
        if param == 0:
            abort(400, 'Parameter %s cannot be 0' % name)  # Bad request

    except TypeError and ValueError:
        logger.exception('Failed to parse %s to integer' % name)
        # Bad request
        abort(400, 'Parameter %s must be integer greater than 0' % name)


def _get_tag(element, selector):
    return element.select_one(selector)


def _get_text(element, selector):
    return _get_tag(element, selector).get_text()


def _flatmap(input_list):
    """[[a, b], [c, d]] -> [a, b, c, d]"""
    return reduce(list.__add__, input_list)
