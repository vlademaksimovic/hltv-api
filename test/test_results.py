import unittest
import json
from unittest import mock
from unittest.mock import MagicMock
from bs4 import BeautifulSoup

from src import results, requester


def _mock_response(*args, **kwargs):
    with open('resources/mock_results.html', 'r') as file:
        return BeautifulSoup(file.read(), 'html.parser')


class TestResults(unittest.TestCase):
    @mock.patch('src.requester.request', side_effect=_mock_response)
    def test_correct_response(self, ignored):
        actual = results.get(requester)

        with open('resources/mock_results.json', 'r') as file:
            expected = json.loads(file.read())

        assert actual == expected

    @mock.patch('src.requester.request', side_effect=_mock_response)
    def test_limit_response(self, ignored):
        actual = results.get(requester, limit='2')

        with open('resources/mock_results.json', 'r') as file:
            expected = json.loads(file.read())

        assert actual == expected[:2]

    @mock.patch('src.requester.request', side_effect=_mock_response)
    def test_offset_response(self, ignored):
        module_to_test = requester
        module_to_test.request = MagicMock(return_value=_mock_response())

        results.get(requester, offset='3')

        module_to_test.request.assert_called_with(
            'https://www.hltv.org/results?offset=3')


if __name__ == '__main__':
    unittest.main()
