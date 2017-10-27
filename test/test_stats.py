import unittest
import json
from unittest import mock
from bs4 import BeautifulSoup

from src import stats, requester


def _mock_stats_response(*args, **kwargs):
    with open('resources/mock_stats.html', 'r') as file:
        return BeautifulSoup(file.read(), 'html.parser')


class TestStats(unittest.TestCase):
    @mock.patch('src.requester.request', side_effect=_mock_stats_response)
    def test_players_correct_response(self, ignored):
        actual = stats.get(requester, type_='players')

        with open('resources/mock_stats_players.json', 'r') as file:
            expected = json.loads(file.read())

        assert actual == expected

    @mock.patch('src.requester.request', side_effect=_mock_stats_response)
    def test_teams_correct_response(self, ignored):
        actual = stats.get(requester, type_='teams')

        with open('resources/mock_stats_teams.json', 'r') as file:
            expected = json.loads(file.read())

        assert actual == expected

    @mock.patch('src.requester.request', side_effect=_mock_stats_response)
    def test_stats_correct_response(self, ignored):
        actual = stats.get(requester)

        with open('resources/mock_stats.json', 'r') as file:
            expected = json.loads(file.read())

        assert actual == expected

    @mock.patch('src.requester.request', side_effect=_mock_stats_response)
    def test_players_limit_response(self, ignored):
        actual = stats.get(requester, '2', type_='players')

        with open('resources/mock_stats_players.json', 'r') as file:
            expected = json.loads(file.read())

        limited_result = expected.get('players')[:2]
        expected = {'players': limited_result}

        assert actual == expected

    @mock.patch('src.requester.request', side_effect=_mock_stats_response)
    def test_teams_limit_response(self, ignored):
        actual = stats.get(requester, '2', type_='teams')

        with open('resources/mock_stats_teams.json', 'r') as file:
            expected = json.loads(file.read())

        limited_result = expected.get('teams')[:2]
        expected = {'teams': limited_result}

        assert actual == expected

    @mock.patch('src.requester.request', side_effect=_mock_stats_response)
    def test_stats_limit_response(self, ignored):
        actual = stats.get(requester, '2')

        with open('resources/mock_stats.json', 'r') as file:
            expected = json.loads(file.read())

        limited_players_result = expected.get('players')[:2]
        limited_teams_result = expected.get('teams')[:2]
        expected = {
            'players': limited_players_result,
            'teams': limited_teams_result,
        }

        assert actual == expected


if __name__ == '__main__':
    unittest.main()
