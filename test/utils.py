import hypothesis.strategies as st

non_numerical_alphabet = 'abcdefghijklmnopqrstuvwxyz'


def one_of_all_primitives(additional_type=None):
    if additional_type:
        return st.one_of(
            st.integers(),
            st.floats(),
            st.text(),
            st.booleans(),
            additional_type())
    else:
        return st.one_of(
            st.integers(),
            st.floats(),
            st.text(),
            st.booleans())
