import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import pytest
from main import main
from io import StringIO
import sys


def test_main_with_valid_args(capsys, tmp_path):
    log_file = tmp_path / "test.log"
    log_file.write_text("[2023-01-01 12:00:00] INFO django.requests GET /test")
    
    sys.argv = ["main.py", str(log_file), "--report", "handlers"]
    

    main()
    
    captured = capsys.readouterr()
    assert "Total requests" in captured.out