import re
from collections import defaultdict
from datetime import datetime

from src.config import SUPPORTED_STATES


def filter_by_state(dictionary_input_list: list[dict], state: str = "EXECUTED") -> list[dict]:
    """filters the list of dictionaries by the 'state' parameter, EXECUTED by default"""
    if state not in SUPPORTED_STATES:
        raise ValueError(f"Недопустимое значение параметра state: {state}")
    output_dictionary_list: list = []
    data_unsupported_states = []
    stop_adding_valid_items_flag = False
    for item in dictionary_input_list:
        current_state = item.get("state", None)
        if current_state not in SUPPORTED_STATES:
            data_unsupported_states.append(item)
            stop_adding_valid_items_flag = True
        if stop_adding_valid_items_flag is False and current_state == state:
            output_dictionary_list.append(item)
    if stop_adding_valid_items_flag is True:
        raise ValueError(
            f"Операции {', '.join(str(item.get('id', 'no_id_operation')) for item in data_unsupported_states)} "
            f"содержат некорректное значение state"
        )

    return output_dictionary_list


def sort_by_date(dictionary_input_list: list[dict], is_reversed: bool = True) -> list[dict]:
    """sorts an input dictionary list by key 'date' and value in ISO format
    in descending (default, True) or ascending (False) order"""
    if not isinstance(is_reversed, bool):
        raise ValueError(f"Параметр is_reversed должен быть типа bool, получено: {type(is_reversed).__name__}")

    invalid_items = []
    for item in dictionary_input_list:
        date_str = item.get("date")
        if not isinstance(date_str, str):
            invalid_items.append(item)
            continue
        try:
            datetime.fromisoformat(date_str)
        except ValueError:
            invalid_items.append(item)
    if invalid_items:
        raise ValueError(
            f"Операции {', '.join(str(item.get('id', 'no_id_operation')) for item in invalid_items)} содержат "
            f"некорректный формат даты"
        )

    return sorted(
        dictionary_input_list,
        key=lambda x: datetime.fromisoformat(x["date"]),
        reverse=is_reversed
    )
    # Не использую функцию get_date из модуля widget, т.к. она возвращает только дату
    # в таком случае, операции за один и тот же день могут неверно сортироваться из-за неучёта времени


def search_in_descriptions(data: list[dict], search: str) -> list[dict]:
    if not isinstance(data, list):
        raise ValueError(f"Параметр data должен быть списком, получено: {type(data).__name__}")
    output: list[dict] = []
    for item in data:
        if not isinstance(item, dict):
            raise ValueError(f"Список должен содержать словари, но содержит элементы типа {type(item).__name__}")
        description = item.get("description", None)
        if description is not None and re.search(search, description, re.IGNORECASE):
            output.append(item)
    return output


def count_transactions_in_categories(data: list[dict], categories: list) -> dict[str, int]:
    if not isinstance(data, list):
        raise ValueError(f"Параметр data должен быть списком, получено: {type(data).__name__}")
    if not isinstance(categories, list):
        raise ValueError(f"Параметр categories должен быть списком, получено: {type(categories).__name__}")
    output_count = defaultdict(int)
    for item in data:
        if not isinstance(item, dict):
            raise ValueError(f"Список должен содержать словари, но содержит элементы типа {type(item).__name__}")
        description = item.get("description", None)
        if description is None: continue
        for category in categories:
            if re.search(category, description, re.IGNORECASE):
                output_count[category] += 1
    return output_count
