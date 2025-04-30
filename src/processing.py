from datetime import datetime


def filter_by_state(dictionary_input_list: list[dict], state: str = "EXECUTED") -> list[dict]:
    """filters the list of dictionaries by the 'state' parameter, EXECUTED by default"""
    output_dictionary_list: list = []
    for item in dictionary_input_list:
        if item["state"] == state:
            output_dictionary_list.append(item)

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
