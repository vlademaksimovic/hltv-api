from functools import reduce

BASE_URL = 'https://www.hltv.org'
RESULTS_URL = BASE_URL + '/results'


def get(requester):
    parsed_content = requester.request(RESULTS_URL)
    all_days_results = parsed_content.find_all(
        'div', attrs={'class': 'results-sublist'})

    # Flatmap to not return [[],[]] but instead []
    return reduce(list.__add__, list(map(_parse_results, all_days_results)))


def _parse_results(single_day_results):
    _results = []
    date = single_day_results.select_one('span.standard-headline') \
        .get_text().replace('Results for ', '')

    for match in single_day_results.select('div.result-con'):
        _result = {}

        team1 = _get_text(match, 'div.team1 .team')
        team2 = _get_text(match, 'div.team2 .team')
        event = _get_text(match, 'td.event > span.event-name')
        map = _get_text(match, 'td.star-cell div.map-text')
        match_link = BASE_URL + _get_tag(match, 'a.a-reset').get('href')

        _result.update({
            'date': date,
            'event': event,
            'map': map,
            'match_link': match_link,
            'team1': team1,
            'team2': team2,
        })

        # Result was a tie
        score_tie = _get_tag(match, 'td.result-score > .score-tie')
        if score_tie:
            # Since it was a tie we know that the results are the same
            score = score_tie.get_text()

            _result.update({
                'score_lost': score,
                'score_won': score,
                'result': 'tie',
            })
        else:
            winner = _get_text(match, 'div.team.team-won')
            score_won = _get_text(match, 'td.result-score > span.score-won')
            score_lost = _get_text(match, 'td.result-score > span.score-lost')

            _result.update({
                'score_lost': score_lost,
                'score_won': score_won,
                'winner': winner,
            })

        _results.append(_result)

    return _results


def _get_tag(element, selector):
    return element.select_one(selector)


def _get_text(element, selector):
    return _get_tag(element, selector).get_text()
