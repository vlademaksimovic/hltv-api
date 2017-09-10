import unittest
import json
from unittest import mock
from bs4 import BeautifulSoup

from src import matches, requester


def _mock_live_response(*args, **kwargs):
    with open('resources/mock_matches_live.html', 'r') as file:
        return BeautifulSoup(file.read(), 'html.parser')


def _mock_upcoming_response(*args, **kwargs):
    with open('resources/mock_matches_upcoming.html', 'r') as file:
        return BeautifulSoup(file.read(), 'html.parser')


def _mock_matches_response(*args, **kwargs):
    with open('resources/mock_matches.html', 'r') as file:
        return BeautifulSoup(file.read(), 'html.parser')


class TestMatches(unittest.TestCase):
    @mock.patch('src.requester.request', side_effect=_mock_live_response)
    def test_live_correct_response(self, ignored):
        actual = matches.get(requester, 'live')

        with open('resources/mock_matches_live.json', 'r') as file:
            expected = json.loads(file.read())

        assert actual == expected

    @mock.patch('src.requester.request', side_effect=_mock_upcoming_response)
    def test_upcoming_correct_response(self, ignored):
        actual = matches.get(requester, 'upcoming')

        with open('resources/mock_matches_upcoming.json', 'r') as file:
            expected = json.loads(file.read())

        assert actual == expected

    @mock.patch('src.requester.request', side_effect=_mock_matches_response)
    def test_matches_correct_response(self, ignored):
        actual = matches.get(requester)

        with open('resources/mock_matches.json', 'r') as file:
            expected = json.loads(file.read())

        assert actual == expected

    @mock.patch('src.requester.request', side_effect=_mock_live_response)
    def test_live_limit_response(self, ignored):
        actual = matches.get(requester, 'live', '2')

        with open('resources/mock_matches_live.json', 'r') as file:
            expected = json.loads(file.read())

        limited_result = expected.get('live')[:2]
        expected = {'live': limited_result}

        assert actual == expected

    @mock.patch('src.requester.request', side_effect=_mock_upcoming_response)
    def test_upcoming_correct_response(self, ignored):
        actual = matches.get(requester, 'upcoming', '2')

        with open('resources/mock_matches_upcoming.json', 'r') as file:
            expected = json.loads(file.read())

        limited_result = expected.get('upcoming')[:2]
        expected = {'upcoming': limited_result}

        assert actual == expected

    @mock.patch('src.requester.request', side_effect=_mock_matches_response)
    def test_matches_correct_response(self, ignored):
        actual = matches.get(requester, limit='2')

        with open('resources/mock_matches.json', 'r') as file:
            expected = json.loads(file.read())

        limited_upcoming_result = expected.get('upcoming')[:2]
        limited_live_result = expected.get('live')[:2]
        expected = {'live': limited_live_result,
                    'upcoming': limited_upcoming_result}

        assert actual == expected


if __name__ == '__main__':
    unittest.main()
