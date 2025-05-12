from typing import Any, Optional

import pytest

from src.processing import datetime, filter_by_state, sort_by_date


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
def test_filter_by_state_correct_input(
        input_dictionary_list_correct: list[dict[str, Any]],
        input_state: Optional[str],
        wanted_list: list[dict[str, Any]]
) -> None:
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
def test_filter_by_state_with_invalid_state_param_raises(
        input_dictionary_list_correct: list[dict[str, Any]],
        invalid_state: Any
) -> None:
    with pytest.raises(ValueError) as result_exc_info:
        filter_by_state(input_dictionary_list_correct, state=invalid_state)

    assert str(result_exc_info.value) == f"Недопустимое значение параметра state: {invalid_state}"


# проверка исключения из-за неподдерживаемого значения ключа state в самом списке словарей
def test_filter_by_state_with_unsupported_state_in_data(
        input_dictionary_list_invalid: list[dict[str, Any]]
) -> None:
    with pytest.raises(
            ValueError,
            match="Операции 444444444, 333333333, 888888888 содержат некорректное значение state"
    ):
        filter_by_state(input_dictionary_list_invalid)


# when pointed on pytest.raises accidentally, noticed the 'match' form of asserting exception information
# later on there will be only 'match' constructions, because its more comfortable than using assert


# testing sort_by_date

def test_sort_by_date_descending(input_dictionary_list_correct: list[dict[str, Any]]) -> None:
    result = sort_by_date(input_dictionary_list_correct)
    dates = [datetime.fromisoformat(item["date"]) for item in result]
    assert dates == sorted(dates, reverse=True)


def test_sort_by_date_descending_with_param(input_dictionary_list_correct: list[dict[str, Any]]) -> None:
    result = sort_by_date(input_dictionary_list_correct, is_reversed=True)
    dates = [datetime.fromisoformat(item["date"]) for item in result]
    assert dates == sorted(dates, reverse=True)


def test_sort_by_date_ascending(input_dictionary_list_correct: list[dict[str, Any]]) -> None:
    result = sort_by_date(input_dictionary_list_correct, is_reversed=False)
    dates = [datetime.fromisoformat(item["date"]) for item in result]
    assert dates == sorted(dates)


@pytest.mark.parametrize("invalid_input", [None, "true", 1, 0, [], {}, 3.14])
def test_sort_by_date_invalid_reverse_param(
        input_dictionary_list_correct: list[dict[str, Any]],
        invalid_input: Any
) -> None:
    with pytest.raises(ValueError, match="Параметр is_reversed должен быть типа bool"):
        sort_by_date(input_dictionary_list_correct, is_reversed=invalid_input)


def test_sort_by_date_invalid_dates_raise(input_dictionary_list_invalid: list[dict[str, Any]]) -> None:
    with pytest.raises(
            ValueError,
            match=r"Операции 777777777, 666666666, 555555555 содержат некорректный формат даты"
    ):
        sort_by_date(input_dictionary_list_invalid)


@pytest.mark.parametrize("reverse_parameter", [True, False])
def test_sort_by_date_same_timestamp_stability(
        input_dictionary_list_same_data: list[dict[str, Any]],
        reverse_parameter: bool
) -> None:
    result = sort_by_date(input_dictionary_list_same_data, reverse_parameter)
    ids = [item['id'] for item in result]
    assert ids == [1, 2, 3]  # стабильная сортировка сохраняет порядок
