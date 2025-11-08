import re

from dateutil import parser

from src import masks
from src.config import KNOWN_CARD_PREFIXES


def mask_account_card(card_info: str) -> str:
    """Returns masked account or card number with prefix validation"""

    if not card_info or not re.search(r"\d", card_info):
        raise ValueError("Не найдены цифры в строке")

    stripped = card_info.strip()
    normalized = stripped.lower()

    if normalized.startswith("счет ") or normalized.startswith("счёт "):
        prefix = stripped[:5]  # сохраняем оригинальный регистр
        number_part = stripped[5:].strip()
        return prefix + masks.get_mask_account(number_part)

    matched_prefix = None
    for prefix in sorted(KNOWN_CARD_PREFIXES, key=len, reverse=True):
        if normalized.startswith(prefix):
            matched_prefix = prefix
            break

    if matched_prefix:
        # сохраняем оригинальный регистр префикса
        original_prefix = card_info[:len(matched_prefix)]
        number_part = card_info[len(matched_prefix):].strip()
        return original_prefix + " " + masks.get_mask_card_number(number_part)

    if re.fullmatch(r"\d+", stripped):
        raise ValueError("Не указан тип карты или счёта")

    raise ValueError("Неподдерживаемый формат ввода")


def get_date(input_date_string: str) -> str:
    """extracts date in DD.MM.YYYY format from ISO datetime string"""
    try:
        date_parsed = parser.isoparse(input_date_string)
    except Exception:
        raise ValueError(f"Некорректная дата/время: {input_date_string}")
    return date_parsed.strftime("%d.%m.%Y")
