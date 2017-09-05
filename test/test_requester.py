import pytest
import unittest
from src import requester
from werkzeug.exceptions import InternalServerError


class TestRequester(unittest.TestCase):
    def test_missing_url_arg(self):
        with pytest.raises(Exception) as exception:
            requester.request('')
        assert exception.type is InternalServerError
