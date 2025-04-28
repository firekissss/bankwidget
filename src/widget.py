import re
from _datetime import datetime

import masks


def mask_account_card(card_info: str) -> str:
    first_digit_match = re.search(r'\d', card_info)
    if not first_digit_match:
        raise ValueError("Не найдены цифры в строке")
    first_digit_index = first_digit_match.start()
    if card_info[:4] == "Счет":
        return card_info[:5] + masks.get_mask_account(card_info[5:])
    else:
        return card_info[:first_digit_index] + masks.get_mask_card_number(card_info[first_digit_index:])


def get_date(input_date_string: str) -> str:
    pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+$'
    if not re.fullmatch(pattern, input_date_string):
        raise ValueError("Некорректный формат")
    try:
        date_parsed = datetime.fromisoformat(input_date_string)
    except ValueError:
        raise ValueError("Некорректная дата/время")
    return date_parsed.strftime("%d.%m.%y")
