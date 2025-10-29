# values and ranges that are supported in the project.
from typing import Any

# bank account length range
MIN_ACC_NUMBER_LENGTH = 4
MAX_ACC_NUMBER_LENGTH = 34

# max card number
MAX_CARD_NUMBER = MAX_CARD_NUMBER = 10 ** 16 - 1
# max card number length
MAX_CARD_NUMBER_LENGTH = 16

# card prefixes
KNOWN_CARD_PREFIXES = [
    "maestro",
    "mastercard",
    "visa",
    "visa classic",
    "visa platinum",
    "visa gold",
    "mir"
]

# states of operations
SUPPORTED_STATES = ["EXECUTED", "CANCELED"]


# Обязательные колонки в содержимом импортируемого файла и типы данных в них.
# Если не требуется преобразование типа, указать Any, в колонке после импорта окажется строка.
# 1 - обязательная колонка, проверяется её наличие и содержимое
# 0 - необязательная колонка, проверяется только тип содержимого, если не указан Any
REQUIRED_DATA_IN_TRANSACTIONS = {
    "id": (int, 1),
    "state": (str, 1),
    "date": (str, 1),
    "amount": (float, 1),
    "currency_name": (str, 1),
    "currency_code": (str, 1),
    "from": (Any, 1),
    "to": (Any, 1),
    "description": (Any, 0),
}

# поведение при отсутствии значения в колонке импортируемого файла:
# 0 - автозаполнение отключено: вызывать ошибку и сообщать об отсутствии значения
# 1 - простое автозаполнение: int/float -> 0, str → ""
# 2 - безопасное автозаполнение: любое поле → None
AUTOADD_MISSING_VALUES = 2
# Использовать безопасное автозаполнение (2), если при дальнейшем обращении к итоговому списку словарей
# требуется чёткое указание на отсутствие значения, а не нулевое значение или пустая строка.