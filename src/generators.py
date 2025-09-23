import textwrap
from typing import Iterator

from src.config import MAX_CARD_NUMBER, MAX_CARD_NUMBER_LENGTH


def filter_by_currency(transactions: list[dict], currency: str) -> Iterator[dict]:
    """
    Filter a list of transaction dictionaries by a specific currency code.

    :param transactions: a list of dictionaries representing transactions
    :param currency: the currency code to filter by (e.g., "USD")
    :return: an iterator over dictionaries matching the specified currency
    """
    if transactions is None:
        raise ValueError("transactions must not be None")
    if not isinstance(currency, str):
        raise TypeError("currency must be a string")

    return (
        t for t in transactions
        if isinstance(t, dict) and t.get("operationAmount", {}).get("currency", {}).get("code") == currency
    )


def transaction_descriptions(transactions: list[dict]) -> Iterator[str]:
    """
    Generator that yields the description of each transaction.

    :param transactions: a list of transaction dictionaries
    :return: an iterator of transaction descriptions
    """
    if transactions is None:
        raise ValueError("transactions must not be None")

    for t in transactions:
        if isinstance(t, dict) and "description" in t:
            yield t["description"]


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """
    Generator that yields a card number in a sequence from start to end

    :param start: the starting point of a sequence
    :param end: the ending point of sequence
    :return: an iterator of card numbers
    """
    if start < 0:
        raise ValueError("card number can't be negative")
    if start > end:
        raise ValueError("start value can't be bigger than end value")
    if end > MAX_CARD_NUMBER:
        raise ValueError(f"card number can't be greater than {MAX_CARD_NUMBER} ({MAX_CARD_NUMBER_LENGTH} digits)")

    for i in range(start, end + 1):
        yield " ".join(textwrap.wrap(f'{i:016d}', 4))


# пример входных данных
transactions = (
    [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702"
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188"
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160"
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {
                "amount": "56883.54",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229"
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {
                "amount": "67314.70",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657"
        }
    ]
)

if __name__ == '__main__':
    for t in filter_by_currency(transactions, "USD"):
        print(t)
    print()
    for d in transaction_descriptions(transactions):
        print(d)
    print()
    for card_number in card_number_generator(9999999999999997, 9999999999999999):
        print(card_number)
