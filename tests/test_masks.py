import pytest

from src import masks


# testing get_mask_card_number

def test_get_mask_card_number_correct(correct_card_number):
    assert masks.get_mask_card_number(correct_card_number) == "1234 56** **** 1121"


@pytest.mark.parametrize("card_number", [
    "12345678901234567890",
    "1234",
])
def test_get_mask_card_number_incorrect_length(card_number):
    with pytest.raises(ValueError) as result_exc_info:
        masks.get_mask_card_number(card_number)

    assert str(result_exc_info.value) == "Номер карты должен содержать 16 цифр"


@pytest.mark.parametrize("some_string", [
    "",
    "123mixedstring",
    "correctlengthstr"
])
def test_get_mask_card_number_no_number(some_string):
    with pytest.raises(ValueError) as result_exc_info:
        masks.get_mask_card_number(some_string)

    assert str(result_exc_info.value) == "Номер карты должен состоять только из цифр"
