import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import pytest
from analyzer import process_files
from collections import defaultdict

def test_process_files(tmp_path):
    log_file = tmp_path / "test.log"
    log_file.write_text(
        "[2023-01-01 12:00:00] INFO django.requests GET /api/test\n"
        "[2023-01-01 12:00:01] ERROR django.requests POST /admin\n"
    )
    
    handlers, total = process_files([log_file])
    
    assert total == 2
    assert handlers["/api/test"]["INFO"] == 1
    assert handlers["/admin"]["ERROR"] == 1

def test_process_files_v2():
    # Создаем временные файлы с логами
    log_content = """
    [2023-01-01 12:00:00] INFO django.requests GET /api/v1/auth/login/
    [2023-01-01 12:00:01] DEBUG django.requests GET /api/v1/auth/login/
    [2023-01-01 12:00:02] WARNING django.requests POST /admin/
    """
    log_file = Path("temp_log.txt")
    log_file.write_text(log_content)

    try:
        handlers_data, total = process_files([log_file])
        assert total == 3
        assert handlers_data["/api/v1/auth/login/"]["INFO"] == 1
        assert handlers_data["/api/v1/auth/login/"]["DEBUG"] == 1
        assert handlers_data["/admin/"]["WARNING"] == 1
    finally:
        log_file.unlink()  # Удаляем временный файл после теста