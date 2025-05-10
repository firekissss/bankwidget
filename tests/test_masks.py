import pytest

from src.masks import get_mask_account, get_mask_card_number

# testing get_mask_card_number

def test_get_mask_card_number_correct(correct_card_number: str) -> None:
    assert get_mask_card_number(correct_card_number) == "1234 56** **** 1121"


@pytest.mark.parametrize("invalid_value, wanted_exc_info", [
    ("", "Номер карты должен состоять только из цифр"),
    ("123mixedstring", "Номер карты должен состоять только из цифр"),
    ("correctlengthstr", "Номер карты должен состоять только из цифр"),

    ("12345678901234567", "Номер карты должен содержать 16 цифр"),
    ("12345678901234567890", "Номер карты должен содержать 16 цифр"),
    ("123456789012345", "Номер карты должен содержать 16 цифр"),
    ("1234", "Номер карты должен содержать 16 цифр")
])
def test_get_mask_card_number_any_invalid_input(invalid_value: str, wanted_exc_info: str) -> None:
    with pytest.raises(ValueError) as result_exc_info:
        get_mask_card_number(invalid_value)

    assert str(result_exc_info.value) == wanted_exc_info


# testing get_mask_account

@pytest.mark.parametrize("account_number, masked_number", [
    ("123456", "**3456"),
    ("12345678901234567890", "**7890")
])
def test_get_mask_account_correct_number(account_number: str, masked_number: str) -> None:
    assert get_mask_account(account_number) == masked_number


@pytest.mark.parametrize("invalid_account_number, wanted_exc_info", [
    ("1234text5678", "Номер счёта должен состоять только из цифр"),
    ("", "Номер счёта должен состоять только из цифр"),
    ("onlytext", "Номер счёта должен состоять только из цифр"),
    (" ", "Номер счёта должен состоять только из цифр"),
    ("anything 123_456?% with space", "Номер счёта должен состоять только из цифр"),

    ("123", "Номер счёта слишком короткий"),
    ("12", "Номер счёта слишком короткий"),
    ("1", "Номер счёта слишком короткий")
])
def test_get_mask_account_any_invalid_input(invalid_account_number: str, wanted_exc_info: str) -> None:
    with pytest.raises(ValueError) as result_exc_info:
        get_mask_account(invalid_account_number)

    assert str(result_exc_info.value) == wanted_exc_info
