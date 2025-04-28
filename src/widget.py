import re
import masks

def mask_account_card(card_info: str) -> str:
    if card_info[:4] == "Счет":
        return card_info[:5] + masks.get_mask_account(card_info[5:])
    else:
        first_digit: int = re.search(r'\d', card_info).start()
        return card_info[:first_digit] + masks.get_mask_card_number(card_info[first_digit:])