import os
from typing import Dict

import requests
from dotenv import load_dotenv


def exchange_through_api(amount, currency, target):
    """
        Convert an amount from one currency to another using the ExchangeRates API.

        :param amount: The numeric amount to convert.
        :param currency: The source currency code (e.g., 'USD').
        :param target: The target currency code (e.g., 'EUR').
        :return: The converted amount as a float.
        :raises RuntimeError: If the API key is missing, request fails, API returns an error,
                              or the result cannot be parsed.
    """
    load_dotenv()
    api_key = os.getenv('APIKEY')
    if not api_key:
        raise RuntimeError("API ключ не найден в .env (переменная APIKEY)")

    url = "https://api.apilayer.com/exchangerates_data/convert"
    payload = {
        "amount": amount,
        "from": currency,
        "to": target
    }
    headers = {"apikey": api_key}
    try:
        response = requests.get(url, headers=headers, params=payload, timeout=5)
        response.raise_for_status()  # выбросит ошибку, если код ответа не 200
    except requests.Timeout:
        raise RuntimeError("Превышено время ожидания ответа от API")
    except requests.ConnectionError:
        raise RuntimeError("Ошибка подключения к интернету или API недоступен")
    except requests.HTTPError as e:
        raise RuntimeError(f"Ошибка HTTP: {e.response.status_code}")

    try:
        data = response.json()
    except ValueError:
        raise RuntimeError("Некорректный JSON в ответе API")

    if not data.get("success"):
        error_info = data.get("error", {})
        raise RuntimeError(f"API вернул ошибку: {error_info}")

    if "result" not in data:
        raise RuntimeError("Ответ не содержит ключ 'result'")

    result_value = data["result"]
    if result_value is None:
        raise RuntimeError("Ключ 'result' содержит пустое значение (None)")

    try:
        return float(result_value)
    except (TypeError, ValueError):
        raise RuntimeError(f"Некорректное значение result: {result_value}")

    # print(status_code)
    # print(result)


def convert_to_rub(transaction: Dict) -> float:
    """
        Convert the amount in a transaction to Russian Rubles (RUB).

        :param transaction: A dictionary representing a transaction,
                            expected to have 'operationAmount' with 'amount' and 'currency'.
        :return: The transaction amount converted to RUB as a float.
        :raises TypeError: If the input is not a dictionary.
        :raises ValueError: If the transaction structure or data types are incorrect.
        :raises RuntimeError: If currency conversion via the API fails.
    """
    if not isinstance(transaction, dict):
        raise TypeError("Ожидался словарь с данными транзакции")

    try:
        op_amount = transaction["operationAmount"]
        amount = float(op_amount["amount"])
        currency = op_amount["currency"]["code"]
    except (KeyError, TypeError, ValueError):
        raise ValueError("Некорректная структура транзакции или тип данных")

    if currency == "RUB":
        return amount

    try:
        return exchange_through_api(amount, currency, "RUB")
    except Exception as e:
        raise RuntimeError(f"Ошибка конвертации валюты: {e}")

# 'operationAmount': {
#      'amount': '31957.58',
#      'currency': {
#          'name': 'руб.', 'code': 'RUB'
#      }
#  }
