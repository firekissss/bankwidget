import re
from unittest.mock import Mock, patch

import pytest
import requests

from src.external_api import convert_to_rub, exchange_through_api


# testing convert_to_rub

# from fixture:
# transactions_fully_correct_data[2] - rub
# transactions_fully_correct_data[0] - usd


def test_convert_to_rub_rub_currency(transactions_fully_correct_data):
    result = convert_to_rub(transactions_fully_correct_data[2])
    assert result == 43318.34


@patch("src.external_api.exchange_through_api", return_value=799389.49)
def test_convert_to_rub_foreign_currency(mock_exchange, transactions_fully_correct_data):
    result = convert_to_rub(transactions_fully_correct_data[0])
    mock_exchange.assert_called_once_with(9824.07, "USD", "RUB")
    assert result == 799389.49


@pytest.mark.parametrize("invalid_input", [None, 123, "string", [1, 2, 3]])
def test_convert_to_rub_invalid_type(invalid_input):
    with pytest.raises(TypeError, match="Ожидался словарь"):
        convert_to_rub(invalid_input)


@pytest.mark.parametrize("bad_transaction", [
    {},  # пусто
    {"operationAmount": None},
    {"operationAmount": {"amount": "100"}},  # нет currency
    {"operationAmount": {"currency": {"code": "RUB"}}},  # нет amount
    {"operationAmount": {"amount": "abc", "currency": {"code": "RUB"}}},  # некорректное число
])
def test_convert_to_rub_invalid_structure(bad_transaction):
    with pytest.raises(ValueError, match="Некорректная структура"):
        convert_to_rub(bad_transaction)


@patch("src.external_api.exchange_through_api", side_effect=RuntimeError)
def test_convert_to_rub_api_error(mock_exchange, transactions_fully_correct_data):
    with pytest.raises(RuntimeError, match="Ошибка конвертации валюты"):
        convert_to_rub(transactions_fully_correct_data[0])
        mock_exchange.assert_called_once()


# testing exchange_through_api

# params with _ in the beginning are implicit mock usages

# correct
@patch("src.external_api.os.getenv", return_value="fake_key")
@patch("src.external_api.load_dotenv")
@patch("src.external_api.requests.get")
def test_exchange_success(mock_get, _mock_load, _mock_env):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "success": True,
        "result": 8137.05
    }
    mock_get.return_value = mock_response

    result = exchange_through_api(100, "USD", "RUB")

    mock_get.assert_called_once()
    assert isinstance(result, float)
    assert result == 8137.05


# no api key
@patch("src.external_api.os.getenv", return_value=None)
@patch("src.external_api.load_dotenv")
def test_exchange_no_api_key(_mock_load, _mock_env):
    with pytest.raises(RuntimeError, match="API ключ не найден"):
        exchange_through_api(100, "USD", "RUB")


# network error/timeout
@pytest.mark.parametrize("side_effect, expected_message", [
    (requests.Timeout, "Превышено время ожидания"),
    (requests.ConnectionError, "Ошибка подключения"),
])
@patch("src.external_api.os.getenv", return_value="fake_key")
@patch("src.external_api.load_dotenv")
@patch("src.external_api.requests.get")
def test_exchange_network_errors(mock_get, _mock_load, _mock_env, side_effect, expected_message):
    mock_get.side_effect = side_effect
    with pytest.raises(RuntimeError, match=expected_message):
        exchange_through_api(100, "USD", "RUB")


# http error
@patch("src.external_api.os.getenv", return_value="fake_key")
@patch("src.external_api.load_dotenv")
@patch("src.external_api.requests.get")
def test_exchange_http_error(mock_get, _mock_load, _mock_env):
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.HTTPError(response=Mock(status_code=404))
    mock_get.return_value = mock_response

    with pytest.raises(RuntimeError, match="Ошибка HTTP: 404"):
        exchange_through_api(100, "USD", "RUB")


# incorrect json response
@patch("src.external_api.os.getenv", return_value="fake_key")
@patch("src.external_api.load_dotenv")
@patch("src.external_api.requests.get")
def test_exchange_invalid_json(mock_get, _mock_load, _mock_env):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.raise_for_status.return_value = None
    mock_response.json.side_effect = ValueError  # incorrect JSON
    mock_get.return_value = mock_response

    with pytest.raises(RuntimeError, match="Некорректный JSON"):
        exchange_through_api(100, "USD", "RUB")


# API error
@patch("src.external_api.os.getenv", return_value="fake_key")
@patch("src.external_api.load_dotenv")
@patch("src.external_api.requests.get")
def test_exchange_api_returns_error(mock_get, _mock_load, _mock_env):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "success": False,
        "error": {"code": 401, "message": "Invalid API key"}
    }
    mock_get.return_value = mock_response

    with pytest.raises(RuntimeError, match="API вернул ошибку"):
        exchange_through_api(100, "USD", "RUB")


# no "result" key in response
@patch("src.external_api.os.getenv", return_value="fake_key")
@patch("src.external_api.load_dotenv")
@patch("src.external_api.requests.get")
def test_exchange_no_result_field(mock_get, _mock_load, _mock_env):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"success": True}
    mock_get.return_value = mock_response

    with pytest.raises(RuntimeError, match="Ответ не содержит ключ 'result'"):
        exchange_through_api(100, "USD", "RUB")


# incorrect "result" value in response
@pytest.mark.parametrize("bad_result", ["abc", {}, [], None])
@patch("src.external_api.os.getenv", return_value="fake_key")
@patch("src.external_api.load_dotenv")
@patch("src.external_api.requests.get")
def test_exchange_invalid_result_value(mock_get, _mock_load, _mock_env, bad_result):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"success": True, "result": bad_result}
    mock_get.return_value = mock_response

    expected_error = (
        "Некорректное значение result"
        if bad_result is not None
        else "Ключ 'result' содержит пустое значение (None)"
    )

    with pytest.raises(RuntimeError, match=re.escape(expected_error)):
        exchange_through_api(100, "USD", "RUB")
