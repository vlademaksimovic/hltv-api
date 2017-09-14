import unittest
import json
import datetime
import pytest
from unittest import mock
from bs4 import BeautifulSoup
from werkzeug.exceptions import BadRequest

from src import news, requester


def _mock_response(*args, **kwargs):
    with open('resources/mock_news_latest.html', 'r') as file:
        return BeautifulSoup(file.read(), 'html.parser')


def _assert_200_response(year, month):
    response = news.get(requester, year=year, month=month)
    assert len(response) == 30


def _assert_bad_request_raised(invalid_year):
    irrelevant_valid_month = 'april'

    with pytest.raises(Exception) as exception:
        news.get(requester, year=invalid_year, month=irrelevant_valid_month)

    assert exception.type is BadRequest


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

        expected = expected[:3]

        assert actual == expected

    @mock.patch('src.requester.request', side_effect=_mock_response)
    def test_year_and_month_response(self, ignored):
        actual = news.get(requester, year='2010', month='april')

        assert len(actual) == 30

    @mock.patch('src.requester.request', side_effect=_mock_response)
    def test_missing_month_response(self, ignored):
        actual = news.get(requester, year='2010')

        assert len(actual) == 30

    @mock.patch('src.requester.request', side_effect=_mock_response)
    def test_valid_responses_with_mixed_args(self, ignored):
        _assert_200_response(year=2010, month='april')
        _assert_200_response(year='2010', month='april')
        _assert_200_response(year=2010, month=None)
        _assert_200_response(year='2010', month=None)
        _assert_200_response(year=None, month='april')

    def test_invalid_year_response(self):
        _assert_bad_request_raised(2004)
        _assert_bad_request_raised((datetime.datetime.now().year + 1))

    def test_invalid_month_response(self):
        valid_year = 2010
        invalid_month = 'non-existing-month'

        with pytest.raises(Exception) as exception:
            news.get(requester, year=valid_year, month=invalid_month)

        assert exception.type is BadRequest


if __name__ == '__main__':
    unittest.main()
