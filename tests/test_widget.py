import pytest

from src.widget import *

@pytest.mark.parametrize("card_or_acc_string, wanted_output", [
    ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
    ("Счет 73654108430135874305", "Счет **4305"),
    ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
    ("Счет 64686473678894779589", "Счет **9589"),
    ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
    ("Счёт 35383033474447895560", "Счёт **5560"),
    ("Visa Classic 6831982476737658", "Visa Classic 6831 98** **** 7658"),
    ("Visa Platinum 8990922113665229", "Visa Platinum 8990 92** **** 5229"),
    ("Visa Gold 5999414228426353", "Visa Gold 5999 41** **** 6353"),
    ("Счёт 73654108430135874305", "Счёт **4305")
])
def test_mask_account_card_correct_values(card_or_acc_string, wanted_output):
    assert mask_account_card(card_or_acc_string) == wanted_output

#errors for incorrect input values of cards and acc numbers are tested in test_masks.py
@pytest.mark.parametrize("incorrect_value, wanted_exc_info", [
    # Нет префикса и есть только номер (номер счёта)
    ("73654108430135874305", "Не указан тип карты или счёта"),
    # Нет префикса и есть только номер (номер карты)
    ("7000792289606361", "Не указан тип карты или счёта"),
    # Есть только префикс "Счет", но нет цифр
    ("Счет", "Не найдены цифры в строке"),
    # Есть только префикс "Счёт", но нет цифр
    ("Счёт", "Не найдены цифры в строке"),
    # Пустая строка
    ("", "Не найдены цифры в строке"),
    # Номер с валидным префиксом, но слишком короткий (некорректный номер карты)
    ("Visa Platinum 1234", "Номер карты должен содержать 16 цифр"),
    # Номер с валидным префиксом, но содержит буквы
    ("Visa Classic 1234abcd5678efgh", "Номер карты должен состоять только из цифр"),
    # Номер с валидным префиксом, но пустой после него
    ("Visa Gold ", "Не найдены цифры в строке"),
    # Номер только с типом карты в другом регистре (но с цифрами)
    ("visa 123456789012345", "Номер карты должен содержать 16 цифр"),
    # Префикс неизвестный
    ("MyCard 1234567890123456", "Неподдерживаемый формат ввода"),
    # Тип "Счёт", но номер слишком короткий
    ("Счёт 123", "Номер счёта слишком короткий"),
    # Тип "Счет", но номер содержит буквы
    ("Счет abc123456789", "Номер счёта должен состоять только из цифр"),
])
def test_mask_account_card_incorrect_input(incorrect_value, wanted_exc_info):
    with pytest.raises(ValueError) as result_exc_info:
        mask_account_card(incorrect_value)
    assert str(result_exc_info.value) == wanted_exc_info
