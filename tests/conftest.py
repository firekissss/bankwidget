import pytest


@pytest.fixture
def correct_card_number() -> str:
    return "1234567891011121"


@pytest.fixture
def input_dictionary_list_correct() -> list[dict[str, str | int]]:
    return [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
        {'id': 999999999, 'state': 'EXECUTED', 'date': '2025-01-01T00:00:00.000000'},
        {'id': 888888888, 'state': 'EXECUTED', 'date': '2023-12-31T23:59:59.999999'}
    ]


@pytest.fixture
def input_dictionary_list_invalid() -> list[dict[str, str | int]]:
    return [
        # incorrect values
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
        {'id': 999999999, 'state': 'EXECUTED', 'date': '2025-01-01T00:00:00.000000'},
        {'id': 777777777, 'state': 'CANCELED', 'date': 'invalid-date'},
        {'id': 666666666, 'state': 'EXECUTED', 'date': '2022-02-29T12:00:00.000000'},  # несуществующая дата
        {'id': 555555555, 'state': 'CANCELED'},  # отсутствует поле date
        {'id': 444444444, 'date': '2020-05-05T05:05:05.555555'},  # отсутствует поле state
        {'id': 333333333, 'state': '', 'date': '2021-11-11T11:11:11.111111'},  # пустой state
        {'id': 888888888, 'state': 'SMTH_UNSUPPORTED', 'date': '2023-12-31T23:59:59.999999'}
        # неподдерживаемое состояние
    ]


@pytest.fixture
def input_dictionary_list_same_data() -> list[dict[str, str | int]]:
    return [
        {'id': 1, 'state': 'EXECUTED', 'date': '2023-01-01T12:00:00.000000'},
        {'id': 2, 'state': 'EXECUTED', 'date': '2023-01-01T12:00:00.000000'},
        {'id': 3, 'state': 'EXECUTED', 'date': '2023-01-01T12:00:00.000000'}
    ]

@pytest.fixture
def transactions_fully_correct_data() -> list[dict]:
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702"
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188"
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160"
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {
                "amount": "56883.54",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229"
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {
                "amount": "67314.70",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657"
        }
    ]
# 3 transactions in USD, 2 in RUB