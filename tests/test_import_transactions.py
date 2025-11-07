import json
import re
from typing import Any
from unittest.mock import mock_open, patch

import pandas as pd
import pytest

import src.config
from src.import_transactions import import_transactions_csv_excel_json


# testing import_transactions_from_file

# тестирование проверок наличия и типов содержимого колонок

# кейс 1: все колонки есть, все типы корректны
@patch("pandas.read_csv")
@patch("pandas.read_excel")
@patch.dict("src.config.REQUIRED_DATA_IN_TRANSACTIONS", {
    "id": (int, 1),
    "state": (str, 1),
    "date": (str, 1),
    "amount": (float, 1),
    "currency_name": (str, 1),
    "currency_code": (str, 1),
    "from": (Any, 1),
    "to": (Any, 1),
    "description": (Any, 0),
}, clear=True)
def test_case_1_all_ok(mock_read_csv, mock_read_excel):
    data = {
        "id": ["1", "2"],
        "state": ["EXECUTED", "CANCELED"],
        "date": ["2024-01-01", "2024-01-02"],
        "amount": ["100.5", "50.0"],
        "currency_name": ["руб.", "USD"],
        "currency_code": ["RUB", "USD"],
        "from": ["acc1", "acc2"],
        "to": ["acc3", "acc4"],
        "description": ["desc1", "desc2"]
    }
    mock_read_csv.return_value = pd.DataFrame(data)
    mock_read_excel.return_value = pd.DataFrame(data)
    result = import_transactions_csv_excel_json("file.csv")
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[0]["operationAmount"]["amount"] == 100.5
    assert result[0]["operationAmount"]["currency"]["name"] == "руб."
    assert result[1]["operationAmount"]["currency"]["code"] == "USD"
    result_2 = import_transactions_csv_excel_json("file.xlsx")
    assert result_2 == result


# кейс 2: только обязательные колонки, типы корректны
@patch("pandas.read_csv")
@patch.dict("src.config.REQUIRED_DATA_IN_TRANSACTIONS", {
    "id": (int, 1),
    "state": (str, 1),
    "date": (str, 1),
    "amount": (float, 1),
    "currency_name": (str, 1),
    "currency_code": (str, 1),
    "from": (Any, 1),
    "to": (Any, 1),
    "description": (Any, 0),
}, clear=True)
def test_case_2_only_required(mock_read_csv):
    data = {
        "id": ["1"],
        "state": ["EXECUTED"],
        "date": ["2024-01-01"],
        "amount": ["10.0"],
        "currency_name": ["руб."],
        "currency_code": ["RUB"],
        "from": ["acc1"],
        "to": ["acc2"],
    }
    mock_read_csv.return_value = pd.DataFrame(data)
    result = import_transactions_csv_excel_json("file.csv")
    assert result[0]["operationAmount"]["amount"] == 10.0


# кейс 3: отсутствуют обязательные колонки
@patch("pandas.read_csv")
@patch.dict("src.config.REQUIRED_DATA_IN_TRANSACTIONS", {
    "id": (int, 1),
    "state": (str, 1),
    "date": (str, 1),
}, clear=True)
def test_case_3_missing_required_columns(mock_read_csv):
    data = {"id": ["1"], "date": ["2024-01-01"]}
    mock_read_csv.return_value = pd.DataFrame(data)
    with pytest.raises(ValueError, match="В файле отсутствуют обязательные колонки: state"):
        import_transactions_csv_excel_json("file.csv")


# кейс 4: неправильный тип в обязательной колонке
@patch("pandas.read_csv")
@patch.dict("src.config.REQUIRED_DATA_IN_TRANSACTIONS", {
    "id": (int, 1),
    "state": (str, 1),
    "date": (str, 1),
    "amount": (float, 1),
    "currency_name": (str, 1),
    "currency_code": (str, 1),
    "from": (Any, 1),
    "to": (Any, 1),
    "description": (Any, 0),
}, clear=True)
def test_case_4_wrong_type_required(mock_read_csv):
    data = {
        "id": ["abc"],  # не получится привести к int
        "state": ["EXECUTED"],
        "date": ["2024-01-01"],
        "amount": ["10.0"],
        "currency_name": ["руб."],
        "currency_code": ["RUB"],
        "from": ["acc1"],
        "to": ["acc2"],
    }
    mock_read_csv.return_value = pd.DataFrame(data)
    with pytest.raises(ValueError, match=re.escape("Ошибка в колонке 'id' строки 0: invalid literal for int() with "
                                                   "base 10: 'abc'")):
        import_transactions_csv_excel_json("file.csv")


# кейс 4.5: неправильный тип в необязательной колонке
@patch("pandas.read_csv")
@patch.dict("src.config.REQUIRED_DATA_IN_TRANSACTIONS", {
    "id": (int, 1),
    "state": (str, 1),
    "date": (str, 1),
    "amount": (float, 1),
    "currency_name": (str, 1),
    "currency_code": (str, 1),
    "from": (int, 1),  # from требуем быть числом
    "to": (Any, 1),
    "description": (Any, 0),
}, clear=True)
def test_case_4_5_wrong_type_optional(mock_read_csv):
    data = {
        "id": ["1", "2"],
        "state": ["EXECUTED", "CANCELED"],
        "date": ["2024-01-01", "2024-01-02"],
        "amount": ["100.5", "50.0"],
        "currency_name": ["руб.", "USD"],
        "currency_code": ["RUB", "USD"],
        "from": ["acc1", "acc2"],  # from - не число
        "to": ["acc3", "acc4"],
        "description": ["desc1", "123"]
    }
    mock_read_csv.return_value = pd.DataFrame(data)
    with pytest.raises(ValueError, match=re.escape("Ошибка в колонке 'from' строки 0: invalid literal for int() with "
                                                   "base 10: 'acc1'")):
        import_transactions_csv_excel_json("file.csv")


# проверка автозаполнения колонок

# кейс 5: в файле содержатся все обязательные колонки, но в одной из строк отсутствует значение (автозаполнение = 0)
@patch("pandas.read_csv")
@patch.dict("src.config.REQUIRED_DATA_IN_TRANSACTIONS", {
    "id": (int, 1),
    "state": (str, 1),
    "date": (str, 1),
    "amount": (float, 1)
}, clear=True)
def test_import_transactions_missing_columns_autoadd_off(mock_read_csv, monkeypatch):
    monkeypatch.setattr("src.config.AUTOADD_MISSING_VALUES", 0)
    data = {
        "id": [None],
        "state": ["CANCELED"],
        "date": ["2024-01-02"],
        "amount": ["50.0"]
    }
    mock_read_csv.return_value = pd.DataFrame(data)
    with pytest.raises(ValueError, match="Отсутствует значение в обязательной колонке 'id' строки 0"):
        import_transactions_csv_excel_json("file.csv")


# кейс 6: в файле содержатся все колонки, но в одной из строк отсутствует значение (автозаполнение = 1)
@patch("pandas.read_csv")
@patch.dict("src.config.REQUIRED_DATA_IN_TRANSACTIONS", {
    "id": (int, 1),
    "state": (str, 1),
    "date": (str, 1),
    "amount": (float, 1)
}, clear=True)
def test_import_transactions_missing_columns_autoadd_mode1(mock_read_csv, monkeypatch):
    monkeypatch.setattr("src.config.AUTOADD_MISSING_VALUES", 1)
    data = {
        "id": [None],
        "state": [None],
        "date": ["2024-01-02"],
        "amount": ["50.0"]
    }
    mock_read_csv.return_value = pd.DataFrame(data)
    result = import_transactions_csv_excel_json("fake.csv")
    assert len(result) == 1
    # в итоговом списке словарей на месте отсутствующего значения получается либо 0
    # (если тип в настройках конфигурации - int или float)
    # либо "" (пустая строка, если любой другой тип в настройках)
    assert "id" in result[0]
    assert result[0]["id"] == 0
    assert "state" in result[0]
    assert result[0]["state"] == ""


# кейс 7: в файле содержатся все колонки, но в одной из строк отсутствует значение (автозаполнение = 2)
@patch("pandas.read_csv")
@patch.dict("src.config.REQUIRED_DATA_IN_TRANSACTIONS", {
    "id": (int, 1),
    "state": (str, 1),
    "date": (str, 1),
    "amount": (float, 1)
}, clear=True)
def test_import_transactions_missing_columns_autoadd_mode2(mock_read_csv, monkeypatch):
    monkeypatch.setattr("src.config.AUTOADD_MISSING_VALUES", 2)
    data = {
        "id": [None],
        "state": [None],
        "date": ["2024-01-02"],
        "amount": ["50.0"]
    }
    mock_read_csv.return_value = pd.DataFrame(data)
    result = import_transactions_csv_excel_json("fake.csv")
    assert len(result) == 1
    # в итоговом списке словарей на месте отсутствующего значения получается либо 0
    # (если тип в настройках конфигурации - int или float)
    # либо "" (пустая строка, если любой другой тип в настройках)
    assert "id" in result[0]
    assert result[0]["id"] is None
    assert "state" in result[0]
    assert result[0]["state"] is None


# проверка ошибок открытия или чтения файла

# кейс 8: введён не тот тип файла (не .csv, не .json и не .xlsx)
def test_case_8_unsupported_filetype():
    with pytest.raises(ValueError, match="Неподдерживаемый тип файла: file.txt. Поддерживаются только .json, .csv и "
                                         ".xlsx."):
        import_transactions_csv_excel_json("file.txt")


# кейс 9: ошибки при открытии или чтении файла
@patch("pandas.read_csv", side_effect=OSError("permission denied"))
def test_case_9_file_open_error(_mock_read_csv):
    with pytest.raises(RuntimeError, match="Ошибка при открытии или чтении файла file.csv: permission denied"):
        import_transactions_csv_excel_json("file.csv")


# кейс 10: файл пустой, результат - пустой список
@patch("pandas.read_csv", side_effect=pd.errors.EmptyDataError)
def test_case_10_empty_file(_mock_read_csv):
    result = import_transactions_csv_excel_json("file.csv")
    assert result == []


# прочие тесты

# кейс 11: на входе .json файл
def test_import_transactions_json_input(transactions_fully_correct_data):
    json_data = json.dumps(transactions_fully_correct_data)
    with patch("builtins.open", mock_open(read_data=json_data)):
        result = import_transactions_csv_excel_json("path.json")
        assert result == transactions_fully_correct_data


# кейс 12: проверка правильности параметра автозаполнения в config.py
@patch("pandas.read_csv")
@patch.dict("src.config.REQUIRED_DATA_IN_TRANSACTIONS", {
    "id": (int, 1),
    "state": (str, 1),
    "date": (str, 1),
    "amount": (float, 1)
}, clear=True)
@pytest.mark.parametrize("wrong_mode", [-1, 500, "строка", None])
def test_import_transactions_wrong_cfg(mock_read_csv, monkeypatch, wrong_mode):
    monkeypatch.setattr("src.config.AUTOADD_MISSING_VALUES", wrong_mode)  # неправильный параметр автозаполнения
    data = {
        "id": [None],
        "state": ["CANCELED"],
        "date": ["2024-01-02"],
        "amount": ["50.0"]
    }
    mock_read_csv.return_value = pd.DataFrame(data)
    e_info = f"Некорректный параметр автозаполнения AUTOADD_MISSING_VALUES: {wrong_mode}. Допустимо 0, 1 или 2"
    with pytest.raises(ValueError, match=e_info):
        import_transactions_csv_excel_json("file.csv")


# кусь 13: ghjdthrf то есть проверка правильности параметров REQUIRED_DATA_IN_TRANSACTIONS (описание колонки)
@pytest.mark.parametrize("invalid_cfg_mandatory_settings, exception_info", [
    ({"id": "строка"}, "Некорректное описание колонки 'id': должно быть кортежем (тип, обязательность)"),
    ({"id": (1, 2, 3)}, "Некорректное описание колонки 'id': должно быть кортежем (тип, обязательность)"),
    ({"id": ("str", 1)}, "Некорректный тип для колонки 'id': str. Должен быть типом (int, float, str, Any или любой "
                         "другой тип)"),
    ({"id": (123, 1)}, "Некорректный тип для колонки 'id': 123. Должен быть типом (int, float, str, Any или любой "
                       "другой тип)"),
    ({"id": (None, 1)}, "Некорректный тип для колонки 'id': None. Должен быть типом (int, float, str, Any или любой "
                        "другой тип)"),
    ({"id": (int, 10000)}, "Некорректный флаг обязательности для колонки 'id': 10000. Допустимо 0 или 1")
])
@patch("pandas.read_csv")
def test_import_transactions_wrong_column_params(mock_read_csv, invalid_cfg_mandatory_settings, exception_info):
    data = {"id": ["1"]}
    mock_read_csv.return_value = pd.DataFrame(data)
    with patch.dict(src.config.REQUIRED_DATA_IN_TRANSACTIONS, invalid_cfg_mandatory_settings, clear=True):
        with pytest.raises(ValueError) as exception_info_result:
            import_transactions_csv_excel_json("file.csv")
        assert exception_info == str(exception_info_result.value)
