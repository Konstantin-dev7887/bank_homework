from __future__ import annotations

from functools import wraps
from typing import Callable, ParamSpec, TypeVar

OK_SUFFIX: str = " ok"
ERR_PREFIX: str = " error:"
INPUTS_LABEL: str = " Inputs:"

P = ParamSpec("P")
R = TypeVar("R")


def log(filename: str | None = None) \
        -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Декоратор логирует результат выполнения функции:
      - <func_name> ok               — при успехе
      - <func_name> error: <Type>.
      Inputs: (<args>), {<kwargs>} — при исключении

    :param filename: путь к файлу для логов; если None — печать в консоль.
    """

    def decorator(function: Callable[P, R]) -> Callable[P, R]:
        @wraps(function)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            try:
                result = function(*args, **kwargs)
                _write(f"{function.__name__}{OK_SUFFIX}", filename)
                return result
            except Exception as exception:
                message = (
                    f"{function.__name__}{ERR_PREFIX} "
                    f"{type(exception).__name__}: {exception}. "
                    f"{INPUTS_LABEL} {args}, {kwargs}"
                )
                _write(message, filename)
                raise

        return wrapper

    return decorator


def _write(message: str, filename: str | None) -> None:
    """Записывает сообщение либо в файл, либо в stdout."""
    if filename:
        with open(filename, "a", encoding="utf-8") as fh:
            fh.write(message + "\n")
    else:
        print(message)
