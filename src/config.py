# values and ranges that are supported in the project.

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
