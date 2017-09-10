import unittest
import json
from unittest import mock
from bs4 import BeautifulSoup

from src import rankings, requester


def _mock_response(*args, **kwargs):
    with open('resources/mock_rankings.html', 'r') as file:
        return BeautifulSoup(file.read(), 'html.parser')


class TestRankings(unittest.TestCase):
    @mock.patch('src.requester.request', side_effect=_mock_response)
    def test_correct_response(self, ignored):
        actual = rankings.get(requester)

        with open('resources/mock_rankings.json', 'r') as file:
            expected = json.loads(file.read())

        assert actual == expected

    @mock.patch('src.requester.request', side_effect=_mock_response)
    def test_limit_response(self, ignored):
        actual = rankings.get(requester, 3)

        expected = json.loads(json.dumps(
            [{'name': 'SK', 'points': 886, 'position': 1},
             {'name': 'G2', 'points': 737, 'position': 2},
             {'name': 'Astralis', 'points': 670, 'position': 3}, ]))

        assert actual == expected


if __name__ == '__main__':
    unittest.main()
