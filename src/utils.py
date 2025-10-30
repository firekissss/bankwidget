import json
import logging
import os
from typing import Dict, List


log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'utils.log')

utils_logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(log_file, mode='w')
file_formatter = logging.Formatter('%(asctime)s:%(filename)s:%(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
utils_logger.addHandler(file_handler)
utils_logger.setLevel(logging.DEBUG)


def get_transactions_from_json(path: str) -> List[Dict]:
    """
       Load a list of transactions from a JSON file.

       :param path: Path to the JSON file containing transaction data.
       :return: A list of dictionaries representing transactions. Returns an empty list if the file
                is not found, cannot be decoded, or does not contain a list.
    """
    utils_logger.debug(f"Attempting to load transactions from {path}")
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                utils_logger.info(f"Successfully loaded {len(data)} transactions from {path}")
                return data
            else:
                utils_logger.warning(f"Invalid data format in {path}: expected list, got {type(data).__name__}")
            # Поставил уровень WARNING здесь и далее в этой функции, т.к. она обрабатывает
            # исключения "в тихую", не выбрасывая исключение, просто возвращает пустой список.
            # Считаю целесообразным выводить в лог предупреждение, а не ошибку.
    except FileNotFoundError:
        utils_logger.warning(f"File not found: {path}")
    except json.JSONDecodeError as e:
        utils_logger.warning(f"Failed to decode JSON from {path}: {e}")

    utils_logger.debug(f"Returning empty transaction list for {path}")
    return []
