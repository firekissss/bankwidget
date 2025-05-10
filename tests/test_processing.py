import pytest

from src.processing import *


# testing filter_by_state

@pytest.mark.parametrize("input_state, wanted_list", [
    (None, [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 999999999, 'state': 'EXECUTED', 'date': '2025-01-01T00:00:00.000000'},
        {'id': 888888888, 'state': 'EXECUTED', 'date': '2023-12-31T23:59:59.999999'}
    ]
     ),  # без указания параметра state (значение EXECUTED по умолчанию)
    ("EXECUTED", [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 999999999, 'state': 'EXECUTED', 'date': '2025-01-01T00:00:00.000000'},
        {'id': 888888888, 'state': 'EXECUTED', 'date': '2023-12-31T23:59:59.999999'}
    ]
     ),
    ("CANCELED", [
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
    ]
     )
])
def test_filter_by_state_correct_input(input_dictionary_list_correct, input_state, wanted_list):
    if input_state is None:  # ветка без указания параметра state (значение EXECUTED по умолчанию)
        assert filter_by_state(input_dictionary_list_correct) == wanted_list
    else:
        assert filter_by_state(input_dictionary_list_correct, state=input_state) == wanted_list


# Проверка неподдерживаемых значений параметра state
@pytest.mark.parametrize("invalid_state", [
    "SMTH_UNSUPPORTED",
    "",
    None
])
def test_filter_by_state_with_invalid_state_param_raises(input_dictionary_list_correct, invalid_state):
    with pytest.raises(ValueError) as result_exc_info:
        filter_by_state(input_dictionary_list_correct, state=invalid_state)

    assert str(result_exc_info.value) == f"Недопустимое значение параметра state: {invalid_state}"


# проверка исключения из-за неподдерживаемого значения ключа state в самом списке словарей
def test_filter_by_state_with_unsupported_state_in_data(input_dictionary_list_invalid):
    with pytest.raises(
            ValueError,
            match="Операции 444444444, 333333333, 888888888 содержат некорректное значение state"
    ):
        filter_by_state(input_dictionary_list_invalid)

# when pointed on pytest.raises accidentally, noticed the 'match' form of asserting exception information
# later on there will be only 'match' constructions, because it's more comfortable than using assert below pytest.raises

