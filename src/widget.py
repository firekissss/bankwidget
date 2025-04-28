import re
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