import unittest
import pytest
from hypothesis import given
import hypothesis.strategies as st

from src.utils import get_milliseconds_delta, get_count, extract_digits
from test.utils import one_of_all_primitives, non_numerical_alphabet


class TestUtils(unittest.TestCase):
    @given(st.datetimes(), st.datetimes())
    def test_get_milliseconds_delta_valid_input_types(self, start, end):
        assert isinstance(get_milliseconds_delta(start, end), float)

    @given(one_of_all_primitives(), one_of_all_primitives())
    def test_get_milliseconds_delta_invalid_input_types(self, start, end):
        with pytest.raises(Exception) as exception:
            get_milliseconds_delta(start, end)
        assert exception.type is TypeError

    @given(st.one_of(st.lists(one_of_all_primitives()), st.none()))
    def test_get_count(self, list_or_none):
        result = get_count(list_or_none)
        assert isinstance(result, int)
        assert result >= 0

    @given(st.text(non_numerical_alphabet),
           st.integers(0),
           st.text(non_numerical_alphabet))
    def test_extract_digits(self, text_start, integer, text_end):
        input_str = text_start + str(integer) + text_end
        result = extract_digits(input_str)
        assert result == str(integer)


if __name__ == '__main__':
    unittest.main()
