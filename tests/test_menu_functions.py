from unittest.mock import patch

import pytest

from src.menu_functions import (
    choose_file,
    exc_msg_dialog,
    filter_by_state_dialog,
    filter_currency_dialog,
    filter_description_dialog,
    filter_dialog,
    formatted_transaction_output,
    handle_cached_import,
    is_transaction_empty,
    load_cache,
    load_transactions,
    print_transactions,
    remove_empty_transactions,
    save_cache,
    sort_transactions_dialog,
)


# testing save_cache and load_cache

def test_save_and_load_cache(tmp_path):
    temp_cache_file = tmp_path / "cache.json"
    data = [{"id": 1, "amount": 100}, {"id": 2, "amount": 200}]
    source_filename = "test_file.csv"
    save_cache(data, source_filename, cache_file_path=temp_cache_file)
    assert temp_cache_file.exists()
    loaded = load_cache(cache_file_path=temp_cache_file)
    assert loaded["source"] == source_filename
    assert loaded["transactions"] == data


def test_load_cache_file_not_exist(tmp_path):
    temp_cache_file = tmp_path / "nonexistent_cache.json"
    result = load_cache(cache_file_path=temp_cache_file)
    assert result is None


# testing exc_msg_dialog

def test_exc_msg_dialog_user_selects_no(capsys):
    with patch("builtins.input", return_value='0'):
        exc_msg_dialog("Ошибка!", "Stack trace")
    captured = capsys.readouterr()
    assert "Ошибка!" in captured.out
    assert "Stack trace" not in captured.out


def test_exc_msg_dialog_user_selects_yes(capsys):
    with patch("builtins.input", side_effect=['1', '']):
        exc_msg_dialog("Ошибка!", "Stack trace")
    captured = capsys.readouterr()
    assert "Ошибка!" in captured.out
    assert "Stack trace" in captured.out


# testing is_transaction_empty

@pytest.mark.parametrize(
    "transaction, expected",
    [
        ({}, True),  # пустой словарь
        ({'a': None, 'b': ""}, True),  # все значения пустые
        ({'a': [], 'b': {}}, True),  # пустые список и словарь
        ({'a': 0, 'b': ""}, False),  # хотя бы одно значимое значение
        ({'a': "something", 'b': {}}, False),  # хотя бы одно значимое значение
        ({'a': {'b': {'c': None}}, 'd': {}}, True),  # вложенные пустые словари
        ({'a': {'b': {'c': 123}}, 'd': {}}, False),  # вложенные словари с хотя бы одним значением
    ]
)
def test_is_transaction_empty(transaction, expected):
    assert is_transaction_empty(transaction) is expected


# testing formatted_transaction_output

@pytest.mark.parametrize("transaction, expected", [
    ({}, "Пустая операция."),  # полностью пустой
    ({"date": ""}, "Дата не указана или формат неверный."),  # неправильная дата
    ({"description": ""}, "Описание отсутствует"),  # пустое описание
    ({"from": "1234"}, "Снятие средств"),  # только отправитель
    ({"to": "5678"}, "Перевод средств"),  # только получатель
    ({"from": "1111", "to": "2222"}, "masked(1111) -> masked(2222)"),  # и то и то
    ({"operationAmount": {}}, "Сумма:\tотсутствует"),  # нет суммы
    ({"operationAmount": {"amount": "100", "currency": {"name": "RUB"}}}, "100 RUB"),  # есть сумма
])
def test_formatted_transaction_output_various(transaction, expected):
    result = formatted_transaction_output(transaction)
    assert expected in result


def test_formatted_transaction_output_valid_full():
    """Полная корректная транзакция."""
    transaction = {
        "date": "2025-01-01T12:00:00",
        "description": "Перевод клиенту",
        "from": "123456",
        "to": "654321",
        "operationAmount": {"amount": "500", "currency": {"name": "USD"}},
    }

    result = formatted_transaction_output(transaction)

    assert "01.01.2025" in result
    assert "Перевод клиенту" in result
    assert "masked(123456)" in result
    assert "masked(654321)" in result
    assert "500 USD" in result


# testing remove_empty_transactions

@pytest.mark.parametrize(
    "transactions, expected_result, expected_print",
    [
        # Все транзакции пустые
        ([{}, {"a": None}], [], "Пустые транзакции (2), не содержащие никаких данных, будут удалены.\n"),

        # Есть и пустые, и непустые
        ([{}, {"id": 1}, {"data": ""}], [{"id": 1}],
         "Пустые транзакции (2), не содержащие никаких данных, будут удалены.\n"),

        # Нет пустых транзакций
        ([{"id": 1}, {"id": 2}], [{"id": 1}, {"id": 2}], None),

        # Пустой список (вообще без транзакций)
        ([], [], None),
    ],
)
def test_remove_empty_transactions(monkeypatch, capsys, transactions, expected_result, expected_print):
    """Проверяет корректное удаление пустых транзакций и сообщение в консоль."""

    # подменим is_transaction_empty, чтобы не зависеть от её реализации
    def fake_is_empty(t):
        # считаем пустыми словари без ключей или с None/пустыми строками
        return not any(v not in (None, "", []) for v in t.values())

    monkeypatch.setattr("src.menu_functions.is_transaction_empty", fake_is_empty)

    # вызываем тестируемую функцию
    result = remove_empty_transactions(transactions)

    # проверяем результат
    assert result == expected_result

    # проверяем, что печать совпала (если должна быть)
    captured = capsys.readouterr()
    if expected_print:
        assert expected_print in captured.out
    else:
        assert captured.out == ""


# testing filter_by_state_dialog

@pytest.mark.parametrize(
    "user_inputs, mock_behavior, expected_result, expected_print_fragment",
    [
        # пользователь вводит 0 — фильтрации нет
        (["0"], {"filter_by_state": None}, [{"id": 1}], "продолжения без фильтрации"),

        # нормальная фильтрация по EXECUTED
        (["EXECUTED"], {"filter_by_state": [{"id": 2}]}, [{"id": 2}], "Операции успешно отфильтрованы"),

        # filter_by_state выбрасывает ValueError
        (["WRONG", "0"], {"filter_by_state": ValueError("Неверный статус")}, [{"id": 1}], "Неверный статус"),

        # filter_by_state выбрасывает Exception, но пользователь выбирает пропуск
        (["EXECUTED", "1"], {"filter_by_state": Exception("Ошибка фильтрации")}, [{"id": 1}], "Пропустить фильтрацию"),

        # filter_by_state выбрасывает Exception, но пользователь выбирает повтор
        (["EXECUTED", "0", "0"], {"filter_by_state": Exception("Ошибка фильтрации")}, [{"id": 1}],
         "Пропустить фильтрацию"),

        # filter_by_state выбрасывает Exception, пользователь выбирает выйти в главное меню
        (["EXECUTED", "2"], {"filter_by_state": Exception("Ошибка фильтрации")}, None, "Пропустить фильтрацию"),
    ],
)
def test_filter_by_state_dialog(monkeypatch, capsys, user_inputs, mock_behavior, expected_result,
                                expected_print_fragment):
    """Проверяет разные сценарии работы filter_by_state_dialog с эмуляцией ввода."""

    transactions = [{"id": 1}]

    # замокаем filter_by_state
    if isinstance(mock_behavior["filter_by_state"], Exception):
        def fake_filter_by_state(*_):
            raise mock_behavior["filter_by_state"]
    elif (isinstance(mock_behavior["filter_by_state"], type)
          and issubclass(mock_behavior["filter_by_state"], Exception)):
        def fake_filter_by_state(*_):
            raise mock_behavior["filter_by_state"]("Ошибка фильтрации")
    elif mock_behavior["filter_by_state"] is None:
        def fake_filter_by_state(*_):
            return transactions
    else:
        def fake_filter_by_state(*_):
            return mock_behavior["filter_by_state"]

    monkeypatch.setattr("src.menu_functions.filter_by_state", fake_filter_by_state)

    # подменим exc_msg_dialog, чтобы не выводил ничего реального
    monkeypatch.setattr("src.menu_functions.exc_msg_dialog", lambda *a, **kw: None)

    # эмулируем ввод
    inputs_iter = iter(user_inputs)
    monkeypatch.setattr("builtins.input", lambda *_: next(inputs_iter))

    # вызываем тестируемую функцию
    result = filter_by_state_dialog(transactions)

    # проверяем результат
    assert result == expected_result

    # проверяем вывод
    out = capsys.readouterr().out
    assert expected_print_fragment in out


# testing sort_transactions_dialog

@pytest.mark.parametrize(
    "user_inputs, expected_is_reversed",
    [
        (["0"], None),  # не сортировать
        (["1", "0"], True),  # сортировать, но не менять порядок (по убыванию)
        (["1", "1"], False)  # сортировать, поменять порядок (по возрастанию)
    ],
)
def test_sort_transactions_dialog(monkeypatch, capsys, user_inputs, expected_is_reversed):
    """Проверка диалога сортировки по дате."""
    transactions = [{"id": 1}, {"id": 2}]

    called = {}

    def fake_sort_by_date(trans, is_reversed):
        called["called"] = True
        called["trans"] = trans
        called["is_reversed"] = is_reversed

    # подмена sort_by_date
    monkeypatch.setattr("src.menu_functions.sort_by_date", fake_sort_by_date)

    # эмуляция ввода
    inputs = iter(user_inputs)
    monkeypatch.setattr("builtins.input", lambda *_: next(inputs))

    # запуск
    sort_transactions_dialog(transactions)

    # вывод
    out = capsys.readouterr().out

    # проверка
    if expected_is_reversed is None:
        # сортировка не вызывается
        assert "Сортировка" not in out or "по убыванию" not in out
        assert "called" not in called
    else:
        assert called["called"]
        assert called["trans"] == transactions
        assert called["is_reversed"] == expected_is_reversed
        assert "Сортировка по убыванию" in out


# testing filter_currency_dialog

@pytest.mark.parametrize(
    "inputs, convert_raises, expected_func, expected_count",
    [
        # пользователь не хочет фильтровать
        (["0"], False, None, 1),
        # хочет только рублевые, без конвертации
        (["1", "0"], False, "filter_by_currency", 1),
        # хочет конвертировать, всё ок
        (["1", "1"], False, "convert_to_rub", 2),
        # конвертация падает, пользователь пробует снова — удачно
        (["1", "1", "1"], True, "convert_to_rub", 3),
        # конвертация падает, пользователь пропускает
        (["1", "1", "0"], True, None, 1),
    ],
)
def test_filter_currency_dialog(monkeypatch, capsys, inputs, convert_raises, expected_func, expected_count):
    """Проверка диалога фильтрации по валюте."""
    transactions = [{"id": 1}, {"id": 2}]
    calls = {"convert": 0, "filter": 0, "exc": 0}

    # --- моки ---
    def fake_convert_to_rub(t):
        calls["convert"] += 1
        if convert_raises and calls["convert"] == 1:
            raise ValueError("API error")
        return {"converted": True}

    def fake_filter_by_currency(trans, cur):
        calls["filter"] += 1
        assert cur == "RUB"
        return [{"filtered": True}]

    def fake_exc_msg_dialog(e, tb):
        calls["exc"] += 1
        print(f"[exc_msg_dialog called: {e}]")

    # подмена функций
    monkeypatch.setattr("src.menu_functions.convert_to_rub", fake_convert_to_rub)
    monkeypatch.setattr("src.menu_functions.filter_by_currency", fake_filter_by_currency)
    monkeypatch.setattr("src.menu_functions.exc_msg_dialog", fake_exc_msg_dialog)

    # эмуляция ввода
    monkeypatch.setattr("builtins.input", lambda *_: inputs.pop(0))

    # запуск
    result = filter_currency_dialog(transactions)

    # проверки
    if expected_func == "convert_to_rub":
        assert calls["convert"] == expected_count
        assert all("converted" in t for t in result)
    elif expected_func == "filter_by_currency":
        assert calls["filter"] == 1
        assert result == [{"filtered": True}]
    else:
        # либо просто возврат оригинальных транзакций
        assert result == transactions

    # если была ошибка — exc_msg_dialog должен вызваться
    if convert_raises:
        assert calls["exc"] >= 1
    else:
        assert calls["exc"] == 0


# testing filter_description_dialog

@pytest.mark.parametrize(
    "inputs, expected_func, expected_calls",
    [
        (["1", "тест"], "search", 1),  # пользователь вводит 1 и строку фильтра
        (["0"], None, 0),  # пользователь не хочет фильтровать
    ],
)
def test_filter_description_dialog(monkeypatch, inputs, expected_func, expected_calls):
    transactions = [{"description": "тестовая транзакция"}]
    calls = {"search": 0}

    # мокаем input и print
    monkeypatch.setattr("builtins.input", lambda prompt=None: inputs.pop(0))
    monkeypatch.setattr("builtins.print", lambda *a, **k: None)

    # мокаем функцию фильтрации
    def mock_search(trans, pattern):
        calls["search"] += 1
        assert pattern == "тест"
        return [t for t in trans if pattern in t["description"]]

    monkeypatch.setattr("src.menu_functions.search_in_descriptions", mock_search)

    result = filter_description_dialog(transactions)

    if expected_func == "search":
        assert calls["search"] == expected_calls
        # результат должен быть отфильтрован
        assert all("тест" in t["description"] for t in result)
    else:
        # search_in_descriptions не должен вызываться
        assert calls["search"] == 0
        # должен вернуться исходный список
        assert result == transactions


# testing print_transactions

def test_print_transactions_empty(monkeypatch):
    printed = []

    # мок для print
    monkeypatch.setattr("builtins.print", lambda *args, **kwargs: printed.append(args))

    # пустой список
    print_transactions([])
    assert any("Список транзакций пуст" in str(p) for p in printed)


def test_print_transactions_with_items(monkeypatch):
    printed = []
    called = []

    # мок для print
    monkeypatch.setattr("builtins.print", lambda *args, **kwargs: printed.append(args))

    # мок для formatted_transaction_output
    def mock_formatted(transaction):
        called.append(transaction)
        return f"mocked output for {transaction.get('id', 'no_id')}"

    monkeypatch.setattr("src.menu_functions.formatted_transaction_output", mock_formatted)

    transactions = [
        {"id": 1, "description": "Test 1"},
        {"id": 2, "description": "Test 2"}
    ]

    print_transactions(transactions)

    # проверяем, что вызвалась наша мок-функция
    assert called == transactions

    # проверяем, что в print попал итоговый заголовок
    assert any("Итоговый список транзакций" in str(p) for p in printed)

    # проверяем, что в print попали строки из мок-функции
    for t in transactions:
        assert any(f"mocked output for {t.get('id')}" in str(p) for p in printed)


def test_print_transactions_with_exception(monkeypatch):
    printed = []
    exc_called = []

    # мок для print
    monkeypatch.setattr("builtins.print", lambda *args, **kwargs: printed.append(args))

    # мок для formatted_transaction_output, выбрасывающий исключение
    def mock_formatted(transaction):
        raise ValueError("test error")

    monkeypatch.setattr("src.menu_functions.formatted_transaction_output", mock_formatted)

    # мок для exc_msg_dialog
    def mock_exc_msg(short, exc_info_stack):
        exc_called.append((short, exc_info_stack))

    monkeypatch.setattr("src.menu_functions.exc_msg_dialog", mock_exc_msg)

    transactions = [
        {"id": 1, "description": "Test 1"},
        {"id": 2, "description": "Test 2"}
    ]

    print_transactions(transactions)

    # проверяем, что наш мок exc_msg_dialog был вызван дважды (по одному разу на транзакцию)
    assert len(exc_called) == 2
    for short, stack in exc_called:
        assert "test error" in str(short)


# testing choose_file

def test_choose_file_cancel(monkeypatch):
    # сценарий, когда пользователь вводит '0'
    monkeypatch.setattr("builtins.input", lambda _: '0')
    result = choose_file()
    assert result is None


def test_choose_file_valid_path(monkeypatch):
    # сценарий, когда пользователь вводит путь к файлу
    monkeypatch.setattr("builtins.input", lambda _: "/path/to/file.csv")
    result = choose_file()
    assert result == "/path/to/file.csv"


# testing load_transactions

def test_load_transactions_success(monkeypatch):
    dummy_data = [{"id": 1}]

    # Моки
    monkeypatch.setattr("src.menu_functions.import_transactions_csv_excel_json", lambda path: dummy_data)
    monkeypatch.setattr("src.menu_functions.save_cache", lambda data, path: None)
    monkeypatch.setattr("src.menu_functions.exc_msg_dialog", lambda e, tb: None)
    monkeypatch.setattr("builtins.print", lambda *a, **k: None)

    result = load_transactions("dummy_path.csv")
    assert result == dummy_data


def test_load_transactions_exception(monkeypatch):
    # Моки
    def mock_import(path):
        raise ValueError("Ошибка импорта")

    called = {"exc_called": False}

    def mock_exc_msg(e, tb):
        called["exc_called"] = True

    monkeypatch.setattr("src.menu_functions.import_transactions_csv_excel_json", mock_import)
    monkeypatch.setattr("src.menu_functions.save_cache", lambda data, path: None)
    monkeypatch.setattr("src.menu_functions.exc_msg_dialog", mock_exc_msg)

    result = load_transactions("dummy_path.csv")
    assert result is None
    assert called["exc_called"] is True


# testing handle_cached_import

def test_handle_cached_import_no_cache(monkeypatch):
    monkeypatch.setattr("src.menu_functions.load_cache", lambda: None)
    monkeypatch.setattr("builtins.print", lambda *a, **kw: None)  # чтобы не выводить в тестах
    result = handle_cached_import()
    assert result is None


def test_handle_cached_import_choice_1(monkeypatch):
    fake_cache = {"source": "dummy.csv", "transactions": [{"id": 1}]}
    monkeypatch.setattr("src.menu_functions.load_cache", lambda: fake_cache)
    monkeypatch.setattr("builtins.input", lambda _: '1')
    result = handle_cached_import()
    assert result == fake_cache['transactions']


def test_handle_cached_import_choice_2(monkeypatch):
    fake_cache = {"source": "dummy.csv", "transactions": [{"id": 1}]}
    monkeypatch.setattr("src.menu_functions.load_cache", lambda: fake_cache)
    monkeypatch.setattr("builtins.input", lambda _: '2')
    monkeypatch.setattr("src.menu_functions.load_transactions", lambda path: [{"id": 2}])
    result = handle_cached_import()
    assert result == [{"id": 2}]


def test_handle_cached_import_choice_other(monkeypatch):
    fake_cache = {"source": "dummy.csv", "transactions": [{"id": 1}]}
    monkeypatch.setattr("src.menu_functions.load_cache", lambda: fake_cache)
    monkeypatch.setattr("builtins.input", lambda _: '0')
    result = handle_cached_import()
    assert result is None


# testing filter_dialog

def test_filter_dialog_empty_transactions(monkeypatch):
    # Проверяем поведение на пустом списке
    monkeypatch.setattr("src.menu_functions.remove_empty_transactions", lambda t: t)
    monkeypatch.setattr("builtins.print", lambda *a, **kw: None)
    filter_dialog([])
    # просто проверяем, что функция не падает


def test_filter_dialog_all_filters(monkeypatch, transactions_fully_correct_data):
    # Мокаем все внутренние функции, чтобы они просто возвращали список или делали ничего
    monkeypatch.setattr("src.menu_functions.remove_empty_transactions", lambda t: t)
    monkeypatch.setattr("src.menu_functions.filter_by_state_dialog", lambda t: t)
    monkeypatch.setattr("src.menu_functions.sort_transactions_dialog", lambda t: None)
    monkeypatch.setattr("src.menu_functions.filter_currency_dialog", lambda t: t)
    monkeypatch.setattr("src.menu_functions.filter_description_dialog", lambda t: t)
    monkeypatch.setattr("src.menu_functions.print_transactions", lambda t: None)
    monkeypatch.setattr("builtins.print", lambda *a, **kw: None)

    # Проверяем, что функция отрабатывает без ошибок
    filter_dialog(transactions_fully_correct_data)


def test_filter_dialog_filter_by_state_none(monkeypatch, transactions_fully_correct_data):
    # Сценарий, когда фильтрация по состоянию возвращает None
    monkeypatch.setattr("src.menu_functions.remove_empty_transactions", lambda t: t)
    monkeypatch.setattr("src.menu_functions.filter_by_state_dialog", lambda t: None)
    monkeypatch.setattr("src.menu_functions.sort_transactions_dialog", lambda t: None)
    monkeypatch.setattr("src.menu_functions.filter_currency_dialog", lambda t: t)
    monkeypatch.setattr("src.menu_functions.filter_description_dialog", lambda t: t)
    monkeypatch.setattr("src.menu_functions.print_transactions", lambda t: None)
    monkeypatch.setattr("builtins.print", lambda *a, **kw: None)

    filter_dialog(transactions_fully_correct_data)


def test_filter_dialog_filter_currency_empty(monkeypatch, transactions_fully_correct_data):
    # Сценарий, когда фильтр валют возвращает пустой список
    monkeypatch.setattr("src.menu_functions.remove_empty_transactions", lambda t: t)
    monkeypatch.setattr("src.menu_functions.filter_by_state_dialog", lambda t: t)
    monkeypatch.setattr("src.menu_functions.sort_transactions_dialog", lambda t: None)
    monkeypatch.setattr("src.menu_functions.filter_currency_dialog", lambda t: [])
    monkeypatch.setattr("src.menu_functions.filter_description_dialog", lambda t: t)
    monkeypatch.setattr("src.menu_functions.print_transactions", lambda t: None)
    monkeypatch.setattr("builtins.print", lambda *a, **kw: None)

    filter_dialog(transactions_fully_correct_data)


def test_filter_dialog_filter_description_empty(monkeypatch, transactions_fully_correct_data):
    # Сценарий, когда фильтр описания возвращает пустой список
    monkeypatch.setattr("src.menu_functions.remove_empty_transactions", lambda t: t)
    monkeypatch.setattr("src.menu_functions.filter_by_state_dialog", lambda t: t)
    monkeypatch.setattr("src.menu_functions.sort_transactions_dialog", lambda t: None)
    monkeypatch.setattr("src.menu_functions.filter_currency_dialog", lambda t: t)
    monkeypatch.setattr("src.menu_functions.filter_description_dialog", lambda t: [])
    monkeypatch.setattr("src.menu_functions.print_transactions", lambda t: None)
    monkeypatch.setattr("builtins.print", lambda *a, **kw: None)

    filter_dialog(transactions_fully_correct_data)
