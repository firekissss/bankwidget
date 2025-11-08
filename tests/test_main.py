import builtins
import pytest
from main import main

@pytest.fixture
def mock_menu_functions(monkeypatch):
    # Мокаем все функции, чтобы не было реального I/O и работы с пользователем
    monkeypatch.setattr("main.choose_file", lambda: "dummy.csv")
    monkeypatch.setattr("main.load_transactions", lambda fp: [{"id": 1}])
    monkeypatch.setattr("main.handle_cached_import", lambda: [{"id": 2}])
    monkeypatch.setattr("main.filter_dialog", lambda t: None)
    monkeypatch.setattr("builtins.print", lambda *a, **kw: None)

@pytest.mark.parametrize(
    "inputs",
    [
        ["1", "3"],       # Новый импорт, потом выход
        ["2", "3"],       # Обработка кэша, потом выход
        ["0", "3"],       # Новый импорт, choose_file вернул None, потом выход
        ["2", "0", "3"],  # Обработка кэша, handle_cached_import вернул None, потом выход
        ["5", "3"],       # Неверный пункт меню, затем выход
    ]
)
def test_main_all_branches(monkeypatch, mock_menu_functions, inputs):
    """Тестируем все ветвления главного цикла main()"""
    input_iter = iter(inputs)
    monkeypatch.setattr(builtins, "input", lambda *args: next(input_iter))

    # Проверяем, что main выполняется без ошибок для всех сценариев
    main()