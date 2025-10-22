import json
from typing import Dict, List


def get_transactions_from_json(path: str) -> List[Dict]:
    """
       Load a list of transactions from a JSON file.

       :param path: Path to the JSON file containing transaction data.
       :return: A list of dictionaries representing transactions. Returns an empty list if the file
                is not found, cannot be decoded, or does not contain a list.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return []
