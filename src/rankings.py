import re

URL = 'https://www.hltv.org/ranking/teams'


def get(requester):
    parsed_content = requester.request(URL)

    teams = parsed_content.find_all('div', attrs={'class': 'ranked-team'})

    if len(teams) == 0:
        return None

    return list(map(_parse_team, teams))


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
