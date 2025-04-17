#!/usr/bin/env python3

import sys
import argparse
import logging
from pathlib import Path
from typing import List

from analyzer import process_files
from reports import REPORTS

# Добавляем текущую директорию в sys.path для корректного импорта
sys.path.append(str(Path(__file__).resolve().parent))


def main() -> None:
    parser = argparse.ArgumentParser(description="Django log analyzer")
    parser.add_argument(
        "logs",
        nargs="+",
        help="Paths to log files",
    )
    parser.add_argument(
        "--report",
        required=True,
        choices=list(REPORTS.keys()),
        help="Report type",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable debug output",
    )
    args = parser.parse_args()

    log_level = logging.DEBUG if args.verbose else logging.WARNING
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s %(levelname)s %(message)s",
    )

    paths: List[Path] = []
    for p_str in args.logs:
        p = Path(p_str)
        if not p.exists():
            logging.error("File %s not found", p)
            sys.exit(1)
        paths.append(p)

    handlers_data, total = process_files(paths)
    report = REPORTS[args.report]
    print(report.generate(handlers_data, total))


if __name__ == "__main__":
    main()
