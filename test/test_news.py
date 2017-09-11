import unittest
import json
from unittest import mock
from bs4 import BeautifulSoup

from src import news, requester


def _mock_response(*args, **kwargs):
    with open('resources/mock_news_latest.html', 'r') as file:
        return BeautifulSoup(file.read(), 'html.parser')


class TestNews(unittest.TestCase):
    @mock.patch('src.requester.request', side_effect=_mock_response)
    def test_correct_response(self, ignored):
        actual = news.get(requester)

        with open('resources/mock_news_latest.json', 'r') as file:
            expected = json.loads(file.read())

        assert actual == expected

    @mock.patch('src.requester.request', side_effect=_mock_response)
    def test_limit_response(self, ignored):
        actual = news.get(requester, '3')

        with open('resources/mock_news_latest.json', 'r') as file:
            expected = json.loads(file.read())

        assert actual == expected[:3]


if __name__ == '__main__':
    unittest.main()
