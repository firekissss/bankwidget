import pytest


@pytest.fixture
def correct_card_number():
    return "1234567891011121"


# @pytest.fixture
# def longer_card_number():
#     return "12345678901234567890"
#
#
# @pytest.fixture
# def shorter_card_number():
#     return "1234"
#
#
# @pytest.fixture
# def zero_length_card_number():
#     return ""
