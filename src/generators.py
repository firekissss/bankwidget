from typing import Iterator


def filter_by_currency(transactions: list[dict], currency: str) -> Iterator[dict]:
    if transactions is None:
        raise ValueError("transactions must not be None")
    if not isinstance(currency, str):
        raise TypeError("currency must be a string")

    return (
        t for t in transactions
        if isinstance(t, dict)
           and t.get("operationAmount", {}).get("currency", {}).get("code") == currency
    )