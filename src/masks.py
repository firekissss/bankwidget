def get_mask_card_number(input_card_number: str) -> str:
    """returns masked card number in XXXX XX** **** XXXX format"""
    if not input_card_number.isdigit():
        raise ValueError("Номер карты должен состоять только из цифр")
    if len(input_card_number) != 16:
        raise ValueError("Номер карты должен содержать 16 цифр")
    return input_card_number[:4] + " " + input_card_number[4:6] + "** **** " + input_card_number[-4:]


def get_mask_account(input_account_number: str) -> str:
    """returns masked bank account number in **XXXX format"""
    if not input_account_number.isdigit():
        raise ValueError("Номер счёта должен состоять только из цифр")
    return "**" + input_account_number[-4:]
