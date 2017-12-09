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

BASE_URL = 'https://www.hltv.org'
RESULTS_URL = BASE_URL + '/results'


def get(requester, limit=None, offset=None):
    sanity_check_integer(limit, 'limit')
    sanity_check_integer(offset, 'offset')

    url = '%s?offset=%s' % (RESULTS_URL, str(offset)) if offset \
        else RESULTS_URL

    parsed_content = requester.request(url)
    all_days_results = \
        get_tags(parsed_content, 'div.results > div.results-holder')

    if len(all_days_results) == 0:
        abort(502)  # Bad gateway

    results = flatmap(list(map(_parse_results, all_days_results)))

    # TODO: Find an optimized way of limiting the response
    if limit:
        results = results[:int(limit)]

    return results


def _parse_results(single_day_results):
    try:
        _results = []
        date = get_tag(single_day_results, 'span.standard-headline')
        date = get_text(date)
        date = date.replace('Results for ', '')

        for match in get_tags(single_day_results, 'div.result-con'):
            _result = {}

            team1 = get_text(match, 'div.team1 .team')
            team2 = get_text(match, 'div.team2 .team')
            event = get_text(match, 'td.event > span.event-name')
            map_ = get_text(match, 'td.star-cell div.map-text')
            match_url = \
                BASE_URL + get_attr(get_tag(match, 'a.a-reset'), 'href')

            _result.update({
                'date': date,
                'event': event,
                'map': map_,
                'match_url': match_url,
                'team1': team1,
                'team2': team2,
            })

            # Result was a tie
            score_tie = get_tag(match, 'td.result-score > .score-tie')
            if score_tie:
                # Since it was a tie we know that the results are the same
                score = score_tie.get_text()

                _result.update({
                    'score_lost': int(score),
                    'score_won': int(score),
                    'result': 'tie',
                })
            else:
                winner = get_text(match, 'div.team.team-won')
                score_won = get_text(
                    match, 'td.result-score > span.score-won')
                score_lost = get_text(
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
