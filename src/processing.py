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
            f"Операции {', '.join(str(item.get("id", "no_id_operation")) for item in data_unsupported_states)} содержат некорректное значение state"
        )

    return output_dictionary_list


def sort_by_date(dictionary_input_list: list[dict], is_reversed: bool = True) -> list[dict]:
    """sorts an input dictionary list by key 'date' and value in ISO format
    in descending (default, True) or ascending (False) order"""
    return sorted(
        dictionary_input_list,
        key=lambda x: datetime.fromisoformat(x["date"]),
        reverse=is_reversed,
    )
    # Не использую функцию get_date из модуля widget, т.к. она возвращает только дату
    # в таком случае, операции за один и тот же день могут неверно сортироваться из-за неучёта времени
