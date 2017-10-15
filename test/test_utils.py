import unittest
import pytest
from bs4 import BeautifulSoup
from hypothesis import given, example
import hypothesis.strategies as st

from src.utils import \
    get_milliseconds_delta, \
    extract_digits, \
    get_count, \
    flatmap, \
    get_tags, \
    get_tag, \
    get_text
from test.utils import \
    one_of_all_primitives, \
    non_numerical_alphabet


class TestUtils(unittest.TestCase):
    @given(st.lists(st.lists(st.integers())))
    @example([])
    @example([[]])
    def test_flatmap(self, list_input):
        for element in list_input:
            assert isinstance(element, list)

        result = flatmap(list_input)
        for element in result:
            assert not isinstance(element, list)
            assert isinstance(element, int)

    def test_get_tag(self):
        html = '<div><span>my-text</span></div>'
        element = BeautifulSoup(html, 'html.parser')
        tag = get_tag(element, 'span')
        assert len(tag) == 1
        assert tag.get_text() == 'my-text'

    def test_get_tags(self):
        html = '<div><span>my-text-1</span><span>my-text-2</span></div>'
        element = BeautifulSoup(html, 'html.parser')
        tags = get_tags(element, 'span')
        assert len(tags) == 2
        assert tags[0].get_text() == 'my-text-1'
        assert tags[1].get_text() == 'my-text-2'

    def test_get_text_with_selector(self):
        html = '<div><span>my-text-1</span></div>'
        element = BeautifulSoup(html, 'html.parser')
        text = get_text(element, 'span')
        assert text == 'my-text-1'

    def test_get_text_without_selector(self):
        html = '<span>my-text-1</span>'
        element = BeautifulSoup(html, 'html.parser')
        text = get_text(element)
        assert text == 'my-text-1'

    @given(st.text(non_numerical_alphabet),
           st.integers(0),
           st.text(non_numerical_alphabet))
    def test_extract_digits(self, text_start, integer, text_end):
        input_str = text_start + str(integer) + text_end
        result = extract_digits(input_str)
        assert result == str(integer)

    @given(st.one_of(st.lists(one_of_all_primitives()), st.none()))
    def test_get_count(self, list_or_none):
        result = get_count(list_or_none)
        assert isinstance(result, int)
        assert result >= 0

    @given(st.datetimes(), st.datetimes())
    def test_get_milliseconds_delta_valid_input_types(self, start, end):
        assert isinstance(get_milliseconds_delta(start, end), float)

    @given(one_of_all_primitives(), one_of_all_primitives())
    def test_get_milliseconds_delta_invalid_input_types(self, start, end):
        with pytest.raises(Exception) as exception:
            get_milliseconds_delta(start, end)
        assert exception.type is TypeError


if __name__ == '__main__':
    unittest.main()
