import json
from unittest.mock import mock_open, patch

from src.utils import get_transactions_from_json


# testing get_transactions_from_json
def test_get_transactions_from_json_correct(transactions_fully_correct_data):
    json_data = json.dumps(transactions_fully_correct_data)
    with patch("builtins.open", mock_open(read_data=json_data)):
        result = get_transactions_from_json("path.json")
        assert result == transactions_fully_correct_data


def test_get_transactions_from_json_incorrect(transactions_data_not_a_list):
    json_data = json.dumps(transactions_data_not_a_list)
    with patch("builtins.open", mock_open(read_data=json_data)):
        result = get_transactions_from_json("path.json")
        assert result == []


def test_get_transactions_from_json_file_not_found():
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = get_transactions_from_json("missing.json")
        assert result == []


def test_get_transactions_from_json_file_json_decode_error():
    with patch("builtins.open", mock_open(read_data="broken_json")):
        with patch("json.load", side_effect=json.JSONDecodeError("msg", "doc", 0)):
            result = get_transactions_from_json("fake.json")
            assert result == []


def test_get_transactions_from_json_file_empty_file():
    with patch("builtins.open", mock_open(read_data="")):
        with patch("json.load", side_effect=json.JSONDecodeError("msg", "doc", 0)):
            result = get_transactions_from_json("empty.json")
            assert result == []
