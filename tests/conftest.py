import pytest


@pytest.fixture
def correct_card_number():
    return "1234567891011121"


@pytest.fixture
def input_dictionary_list_correct():
    return [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
        {'id': 999999999, 'state': 'EXECUTED', 'date': '2025-01-01T00:00:00.000000'},
        {'id': 888888888, 'state': 'EXECUTED', 'date': '2023-12-31T23:59:59.999999'}
    ]


@pytest.fixture
def input_dictionary_list_invalid():
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
def input_dictionary_list_same_data():
    return [
        {'id': 1, 'state': 'EXECUTED', 'date': '2023-01-01T12:00:00.000000'},
        {'id': 2, 'state': 'EXECUTED', 'date': '2023-01-01T12:00:00.000000'},
        {'id': 3, 'state': 'EXECUTED', 'date': '2023-01-01T12:00:00.000000'}
    ]
