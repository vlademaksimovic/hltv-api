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


class TestMatches(unittest.TestCase):
    @mock.patch('src.requester.request', side_effect=_mock_live_response)
    def test_live_filter_correct_response(self, ignored):
        actual = matches.get(requester, 'live')

        with open('resources/mock_matches_live.json', 'r') as file:
            expected = json.loads(file.read())

        assert actual == expected

    @mock.patch('src.requester.request', side_effect=_mock_upcoming_response)
    def test_upcoming_filter_correct_response(self, ignored):
        actual = matches.get(requester, 'upcoming')

        with open('resources/mock_matches_upcoming.json', 'r') as file:
            expected = json.loads(file.read())

        assert actual == expected


if __name__ == '__main__':
    unittest.main()
