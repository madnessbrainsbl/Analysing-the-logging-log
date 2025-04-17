from pathlib import Path
from typing import DefaultDict, Tuple, List
from collections import defaultdict
import logging
from concurrent.futures import ProcessPoolExecutor

LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
HTTP_METHODS = {"GET", "POST", "PUT", "DELETE", "PATCH"}


def default_dict_factory():
    return defaultdict(int)


class LogAnalyzer:
    def __init__(self) -> None:
        self.handlers: DefaultDict[str, DefaultDict[str, int]] = defaultdict(default_dict_factory)
        self.total_requests: int = 0

    def process_line(self, line: str) -> None:
        if "django.requests" not in line:
            return

        parts = line.split()
        if len(parts) < 3:
            logging.debug("Недостаточно частей в строке: %r", line)
            return

        log_level = parts[2]
        if log_level not in LOG_LEVELS:
            logging.debug("Неизвестный уровень %r в строке: %r", log_level, line)
            return

        handler = "unknown"
        for i, part in enumerate(parts):
            if part in HTTP_METHODS and i + 1 < len(parts) and parts[i + 1].startswith("/"):
                handler = parts[i + 1]
                break

        self.handlers[handler][log_level] += 1
        self.total_requests += 1
        logging.debug("Обновлён handler=%r, level=%r", handler, log_level)


def process_file(path: Path) -> Tuple[DefaultDict[str, DefaultDict[str, int]], int]:
    analyzer = LogAnalyzer()
    try:
        with path.open("r", encoding="utf-8") as f:
            for raw in f:
                analyzer.process_line(raw.strip())
    except UnicodeDecodeError:
        with path.open("r", encoding="latin-1") as f:
            for raw in f:
                analyzer.process_line(raw.strip())
    return analyzer.handlers, analyzer.total_requests


def process_files(paths: List[Path]) -> Tuple[DefaultDict[str, DefaultDict[str, int]], int]:
    """
    Параллельно обрабатывает список путей, возвращает объединённые результаты.
    """
    total_handlers: DefaultDict[str, DefaultDict[str, int]] = defaultdict(default_dict_factory)
    total_requests = 0

    with ProcessPoolExecutor() as executor:
        for handlers, cnt in executor.map(process_file, paths):
            for handler, levels in handlers.items():
                for lvl, c in levels.items():
                    total_handlers[handler][lvl] += c
            total_requests += cnt

    return total_handlers, total_requests
