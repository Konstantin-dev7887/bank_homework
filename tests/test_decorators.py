from __future__ import annotations

from pathlib import Path
from typing import Final

import pytest

from src.decorators import log

OK_SUFFIX: Final[str] = " ok"
ERR_PREFIX: Final[str] = " error:"
INPUTS_TOKEN: Final[str] = "Inputs:"


def test_log_console_ok(capsys: pytest.CaptureFixture[str]) -> None:
    @log()
    def add(x: int, y: int) -> int:
        return x + y

    assert add(1, 2) == 3
    out = capsys.readouterr().out.strip()
    assert out == f"{add.__name__}{OK_SUFFIX}"


def test_log_console_error(capsys: pytest.CaptureFixture[str]) -> None:
    @log()
    def div(x: int, y: int) -> int:
        return x // y

    with pytest.raises(ZeroDivisionError):
        div(1, 0)

    out = capsys.readouterr().out.strip()
    assert out.startswith(f"{div.__name__}{ERR_PREFIX}")
    assert INPUTS_TOKEN in out


def test_log_file_ok(path: Path) -> None:
    logfile = path / "mylog.txt"

    @log(filename=str(logfile))
    def mul(x: int, y: int) -> int:
        return x * y

    assert mul(3, 4) == 12

    lines = logfile.read_text(encoding="utf-8").splitlines()
    assert f"{mul.__name__}{OK_SUFFIX}" in lines


def test_log_file_error(path: Path) -> None:
    logfile = path / "mylog.txt"
    message: Final[str] = "boom"

    @log(filename=str(logfile))
    def fail() -> None:
        raise RuntimeError(message)

    with pytest.raises(RuntimeError):
        fail()

    text = logfile.read_text(encoding="utf-8")
    assert text.startswith(f"{fail.__name__}{ERR_PREFIX}")
    assert INPUTS_TOKEN in text and message in text
