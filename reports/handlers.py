from typing import DefaultDict
from collections import defaultdict

from .base import Report

LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class HandlersReport(Report):
    name = "handlers"

    def generate(
        self,
        data: DefaultDict[str, DefaultDict[str, int]],
        total: int
    ) -> str:
        if not data:
            return "No data available for handlers report"

        header = ["HANDLER"] + LOG_LEVELS
        rows: list[list[str]] = []
        for handler in sorted(data.keys()):
            rows.append([handler] + [str(data[handler].get(lvl, 0)) for lvl in LOG_LEVELS])

        totals = [str(sum(int(row[i + 1]) for row in rows)) for i in range(len(LOG_LEVELS))]
        rows.append(["TOTAL"] + totals)

        # Ширины колонок
        col_widths = [
            max(len(header[i]), *(len(row[i]) for row in rows))
            for i in range(len(header))
        ]

        lines: list[str] = [f"Total requests: {total}", ""]
        # Заголовок
        lines.append("  ".join(header[i].ljust(col_widths[i]) for i in range(len(header))))
        # Строки с данными
        for row in rows:
            lines.append("  ".join(row[i].ljust(col_widths[i]) for i in range(len(row))))
        return "\n".join(lines)
