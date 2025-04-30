from datetime import datetime


def filter_by_state(dictionary_input_list: list[dict], state: str = 'EXECUTED') -> list[dict]:
    output_dictionary_list: list = []
    for item in dictionary_input_list:
        if item['state'] == state:
            output_dictionary_list.append(item)

    return output_dictionary_list


def sort_by_date(dictionary_input_list: list[dict], order: str = 'descending') -> list[dict]:
    formatted_order = order.lower()
    if formatted_order not in ('ascending', 'descending'):
        raise ValueError("Аргумент 'order' может быть либо 'ascending', либо 'descending'.")

    return sorted(
        dictionary_input_list,
        key=lambda x: datetime.fromisoformat(x['date']),
        reverse=True if formatted_order == 'descending' else False
    )
