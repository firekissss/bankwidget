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
