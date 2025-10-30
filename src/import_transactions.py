from typing import List, Dict, Any
from src.utils import get_transactions_from_json
from src.config import REQUIRED_DATA_IN_TRANSACTIONS, AUTOADD_MISSING_VALUES

import pandas as pd


def import_transactions_csv_excel(file_path: str) -> List[Dict]:
    if file_path.endswith('.json'):
        return get_transactions_from_json(file_path)
        # обработка ошибок открытия файла .json уже реализована в функции

    if not (file_path.endswith('.csv') or file_path.endswith('.xlsx')):
        raise ValueError(
            f"Неподдерживаемый тип файла: {file_path}. Поддерживаются только .json, .csv и .xlsx."
        )
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path, delimiter=';', dtype=str)
        elif file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path, dtype=str)
    except pd.errors.EmptyDataError:
        return []
    except Exception as e:
        # любая другая ошибка при открытии/чтении файла
        raise RuntimeError(f"Ошибка при открытии или чтении файла {file_path}: {e}") from e

    # Проверка конфигурации REQUIRED_DATA_IN_TRANSACTIONS
    for col, value in REQUIRED_DATA_IN_TRANSACTIONS.items():
        if not isinstance(value, tuple) or len(value) != 2:
            raise ValueError(f"Некорректное описание колонки '{col}': должно быть кортежем (тип, обязательность)")

        col_type, mandatory = value

        if col_type not in [int, float, str, Any]:
            raise ValueError(f"Некорректный тип для колонки '{col}': {col_type}. Допустимо int, float, str, Any")

        if mandatory not in [0, 1]:
            raise ValueError(f"Некорректный флаг обязательности для колонки '{col}': {mandatory}. Допустимо 0 или 1")

    # Проверка AUTOADD_MISSING_VALUES
    if AUTOADD_MISSING_VALUES not in [0, 1, 2]:
        raise ValueError(
            f"Некорректный параметр автозаполнения AUTOADD_MISSING_VALUES: {AUTOADD_MISSING_VALUES}. Допустимо 0, 1 "
            f"или 2")

    # Проверка обязательных колонок на наличие
    required_mandatory_cols = {col for col, (_, mandatory) in REQUIRED_DATA_IN_TRANSACTIONS.items() if mandatory == 1}
    missing = required_mandatory_cols - set(df.columns)
    if missing:
        raise ValueError(f"В файле отсутствуют обязательные колонки: {', '.join(missing)}")

    transactions = []
    for index, row in df.iterrows():
        transaction_data = {}
        for col, (col_type, mandatory) in REQUIRED_DATA_IN_TRANSACTIONS.items():
            value = row.get(col, None)

            # Если в ячейке пустое значение
            if pd.isna(value) or value is None:
                if mandatory == 1 and AUTOADD_MISSING_VALUES == 0:
                    raise ValueError(f"Отсутствует значение в обязательной колонке '{col}' строки {index}")
                elif AUTOADD_MISSING_VALUES == 1:
                    if col_type in [int, float]:
                        value = 0
                    else:
                        value = ""

                elif AUTOADD_MISSING_VALUES == 2:
                    value = None

            # Если в ячейке есть значение, приводим тип, если он указан в конфиге
            else:
                if col_type is not Any:
                    try:
                        value = col_type(value)
                    except (ValueError, TypeError) as e:
                        raise type(e)(f"Ошибка в колонке '{col}' строки {index}: {e}") from e
            transaction_data[col] = value

        # Форматирование итогового словаря
        transaction = {
            "id": transaction_data.get("id"),
            "state": transaction_data.get("state"),
            "date": transaction_data.get("date"),
            "operationAmount": {
                "amount": str(transaction_data.get("amount")),
                "currency": {
                    "name": transaction_data.get("currency_name"),
                    "code": transaction_data.get("currency_code")
                }
            },
            "description": transaction_data.get("description", ""),
            "from": transaction_data.get("from", ""),
            "to": transaction_data.get("to", "")
        }
        transactions.append(transaction)

    return transactions
