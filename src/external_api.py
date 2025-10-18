import os
from typing import Dict

import requests
from dotenv import load_dotenv


def exchange_through_api(amount, currency, target):
    load_dotenv()
    api_key = os.getenv('APIKEY')
    if not api_key:
        raise RuntimeError("API ключ не найден в .env (переменная APIKEY)")

    url = "https://api.apilayer.com/exchangerates_data/convert"
    payload = {
        "amount": amount,###
        "from": currency,
        "to": target
    }
    headers = {"apikey": api_key}
    try:
        response = requests.get(url, headers=headers, params=payload, timeout=5)
        response.raise_for_status()  # выбросит ошибку, если код ответа не 200 ###
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

    result_value = data.get("result")
    if result_value is None:
        raise RuntimeError("Ответ не содержит ключ 'result'")

    try:
        return float(result_value)
    except (TypeError, ValueError):
        raise RuntimeError(f"Некорректное значение result: {result_value}")

    # print(status_code)
    # print(result)


def convert_to_rub(transaction: Dict) -> float:
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
    except RuntimeError as e:
        raise RuntimeError(f"Ошибка конвертации валюты: {e}")

# 'operationAmount': {
#      'amount': '31957.58',
#      'currency': {
#          'name': 'руб.', 'code': 'RUB'
#      }
#  }
