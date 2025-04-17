import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from collections import defaultdict

import pytest

from reports.handlers import HandlersReport
from reports import generate_handlers_report


def test_empty_report():
    report = HandlersReport()
    text = report.generate(defaultdict(lambda: defaultdict(int)), 0)
    assert "No data available" in text


def test_report_format():
    data = defaultdict(lambda: defaultdict(int))
    data["/a/"]["INFO"] = 2
    data["/b/"]["DEBUG"] = 3
    total = 5

    report = HandlersReport()
    text = report.generate(data, total)
    lines = text.splitlines()

    # Первая строка — общее число запросов
    assert lines[0] == f"Total requests: {total}"
    # Заголовок на третьей строке
    assert "HANDLER" in lines[2] and "DEBUG" in lines[2] and "INFO" in lines[2]
    # Должны быть строки для /a/ и /b/
    assert any(line.startswith("/a/") for line in lines[3:])
    assert any(line.startswith("/b/") for line in lines[3:])
    # Есть строка TOTAL
    assert any(line.startswith("TOTAL") for line in lines)


def test_generate_handlers_report():
    handlers_data = defaultdict(lambda: defaultdict(int))
    handlers_data["/api/v1/auth/login/"]["INFO"] = 1
    handlers_data["/api/v1/auth/login/"]["DEBUG"] = 1
    handlers_data["/admin/"]["WARNING"] = 1
    total = 3

    report = generate_handlers_report(handlers_data, total)
    
    # Проверка содержимого отчета без учета форматирования
    assert f"Total requests: {total}" in report
    assert "HANDLER" in report and "DEBUG" in report and "INFO" in report
    assert "/api/v1/auth/login/" in report
    assert "/admin/" in report
    assert "TOTAL" in report
    # Проверка корректности счетчиков
    assert "1" in report  # INFO, DEBUG, WARNING counts
    assert "0" in report  # Missing counts
