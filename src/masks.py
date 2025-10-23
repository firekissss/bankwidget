import logging

from src.config import MAX_ACC_NUMBER_LENGTH, MIN_ACC_NUMBER_LENGTH
from src.decorators import log_exceptions


masks_logger = logging.getLogger(__name__)
file_handler = logging.FileHandler('logs/masks.log')
file_formatter = logging.Formatter('%(asctime)s:%(filename)s:%(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
masks_logger.addHandler(file_handler)
masks_logger.setLevel(logging.DEBUG)


def is_in_allowed_acc_number_range(account_number: str) -> bool:
    """Checks if account number is in allowed range"""
    masks_logger.debug(f'Ckecking if {account_number} is in allowed acc number range')
    return MIN_ACC_NUMBER_LENGTH <= len(account_number) <= MAX_ACC_NUMBER_LENGTH


@log_exceptions(masks_logger)
def get_mask_card_number(input_card_number: str) -> str:
    """returns masked card number in XXXX XX** **** XXXX format"""
    masks_logger.info(f'Getting masked card number from {input_card_number}')

    if not input_card_number.isdigit():
        raise ValueError("Номер карты должен состоять только из цифр")
    if len(input_card_number) != 16:
        raise ValueError("Номер карты должен содержать 16 цифр")

    return input_card_number[:4] + " " + input_card_number[4:6] + "** **** " + input_card_number[-4:]


@log_exceptions(masks_logger)
def get_mask_account(input_account_number: str) -> str:
    """returns masked bank account number in **XXXX format"""
    masks_logger.info(f'Getting masked account number from {input_account_number}')

    if not input_account_number.isdigit():
        raise ValueError("Номер счёта должен состоять только из цифр")
    # минимальная длина счёта - у формата счёта USA - 4 цифры без учёта Routing number (ABA)
    if not is_in_allowed_acc_number_range(input_account_number):
        raise ValueError("Номер счёта слишком короткий")

    return "**" + input_account_number[-4:]
