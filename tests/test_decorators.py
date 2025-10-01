import re

import pytest

from src.decorators import log


# testing date/time format in a log
def test_console_log_contains_date_time(capsys):
    @log()
    def add(a, b=1):
        return a + b

    add(100)
    captured = capsys.readouterr()
    # check if log date/time exists and its format is correct
    assert re.search(r"\[\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}:\d{2}\] Function 'add' called", captured.out)


def test_file_log_contains_date_time(tmp_path):
    log_file = tmp_path / "log.txt"

    @log(filename=str(log_file))
    def add_file(a, b=5):
        return a + b

    add_file(5, b=10)
    assert log_file.exists()
    content = log_file.read_text(encoding='utf-8')
    assert re.search(r"\[\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}:\d{2}\] Function 'add_file' called", content)


# testing successful function call
def test_console_add_log_successful(capsys):
    @log()
    def add(a, b=1):
        return a + b

    result = add(4, b=6)
    captured = capsys.readouterr()
    assert result == 10
    assert "Function 'add' called" in captured.out
    assert "args: (4,)" in captured.out
    assert "kwargs: {'b': 6}" in captured.out
    assert "result: 10" in captured.out


def test_file_add_log_successful(tmp_path):
    log_file = tmp_path / "log.txt"

    @log(filename=str(log_file))
    def add_file(a, b=5):
        return a + b

    result = add_file(5, b=10)
    assert result == 15
    assert log_file.exists()
    content = log_file.read_text(encoding='utf-8')
    assert "Function 'add_file' called" in content
    assert "args: (5,)" in content
    assert "kwargs: {'b': 10}" in content
    assert "result: 15" in content


# testing error logging
def test_console_add_log_error(capsys):
    @log()
    def fail(x):
        raise ValueError("test error")

    with pytest.raises(ValueError, match="test error"):
        fail(1)
    captured = capsys.readouterr()
    assert "Function 'fail' called" in captured.out
    assert "args: (1,)" in captured.out
    assert "kwargs: {}" in captured.out
    assert "error: test error" in captured.out
    assert "Traceback" in captured.out


def test_file_add_log_error(tmp_path):
    log_file = tmp_path / "log.txt"

    @log(filename=str(log_file))
    def fail(x):
        raise ValueError("test error")

    with pytest.raises(ValueError, match="test error"):
        fail(1)

    content = log_file.read_text(encoding="utf-8")
    assert "Function 'fail' called" in content
    assert "args: (1,)" in content
    assert "kwargs: {}" in content
    assert "error: test error" in content
    assert "Traceback" in content
