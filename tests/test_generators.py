import pytest

from src.generators import *
from tests.conftest import transactions_fully_correct_data


# testing filter_by_currency

@pytest.mark.parametrize(
    "currency,expected_count",
    [
        ("USD", 3),
        ("RUB", 2),
        ("EUR", 0)
    ]
)
def test_filter_by_currency_correct_data(transactions_fully_correct_data: list[dict], currency, expected_count) -> None:
    result = list(filter_by_currency(transactions_fully_correct_data, currency))
    assert len(result) == expected_count


def test_filter_by_currency_empty_list():
    """Empty transactions list should not raise errors"""
    result = list(filter_by_currency([], "USD"))
    assert result == []


def test_filter_by_currency_no_currency_field():
    """Transactions without currency info should be skipped silently"""
    transactions = [
        {"operationAmount": {"currency": {"code": "RUB"}}},
        {"noAmountHere": 123},  # некорректная структура
    ]
    result = list(filter_by_currency(transactions, "USD"))
    assert result == []  # не упало, пустой результат на выходе


def test_filter_by_currency_transactions_none():
    """Should raise ValueError if transactions is None"""
    with pytest.raises(ValueError, match="transactions must not be None"):
        list(filter_by_currency(None, "USD"))


@pytest.mark.parametrize("invalid_currency", [123, None, 3.14, ["USD"]])
def test_filter_by_currency_invalid_currency_type(invalid_currency):
    """Should raise TypeError if currency is not a string"""
    with pytest.raises(TypeError, match="currency must be a string"):
        list(filter_by_currency([], invalid_currency))


# testing transaction_descriptions
def test_transaction_descriptions_correct_data(transactions_fully_correct_data):
    assert list(transaction_descriptions(transactions_fully_correct_data)) == [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод со счета на счет",
        "Перевод с карты на карту",
        "Перевод организации"
    ]


def test_transaction_descriptions_step_by_step(transactions_fully_correct_data):
    """testing that the function behaves like a generator, not anything else"""
    gen = transaction_descriptions(transactions_fully_correct_data)

    assert next(gen) == "Перевод организации"
    assert next(gen) == "Перевод со счета на счет"
    assert next(gen) == "Перевод со счета на счет"
    assert next(gen) == "Перевод с карты на карту"
    assert next(gen) == "Перевод организации"

    with pytest.raises(StopIteration):
        next(gen)


@pytest.mark.parametrize(
    "transactions,expected",
    [
        ([], []),  # пустой список
        ([{"description": "Перевод организации"}], ["Перевод организации"]),  # 1 элемент
        (
                [  # 3 элемента
                    {"description": "Перевод организации"},
                    {"description": "Перевод со счета на счет"},
                    {"description": "Перевод с карты на карту"},
                ],
                [
                    "Перевод организации",
                    "Перевод со счета на счет",
                    "Перевод с карты на карту",
                ],
        ),
        (
                [  # один из элементов без description
                    {"description": "Перевод организации"},
                    {"id": 123, "state": "EXECUTED"},
                    {"description": "Перевод с карты на карту"},
                ],
                [
                    "Перевод организации",
                    "Перевод с карты на карту",
                ],
        ),
    ]
)
def test_transaction_descriptions_various_lengths(transactions, expected):
    assert list(transaction_descriptions(transactions)) == expected


def test_transaction_descriptions_none_input():
    with pytest.raises(ValueError, match="transactions must not be None"):
        list(transaction_descriptions(None))
