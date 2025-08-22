from __future__ import annotations

from datetime import datetime

from .masks import get_mask_account, get_mask_card_number


def mask_account_card(account_card: str | int | None) -> str:
    """
    Определяет тип входа и применяет нужную маску.
    - Если это карта (обычно 16+ цифр, присутствуют пробелы/слова Visa/MasterCard и т.п.) - маскирует как карту.
    - Если это счёт (строки, начинающиеся с 'Счет'/'Счёт' или просто длинные числовые строки) - маскирует как счёт.
    Некорректные входы → пустая строка.
    """
    if account_card is None:
        return ""

    account_card_text = str(account_card).strip()
    digits = "".join(symbol for symbol in account_card_text if symbol.isdigit())

    if not digits:
        return ""

    if len(digits) >= 16 or any(k in account_card_text.lower() for k in ("visa", "mastercard", "maestro", "mir")):
        return get_mask_card_number(account_card_text)

    if account_card_text.lower().startswith(("счет", "счёт")) or len(digits) >= 10:
        return get_mask_account(account_card_text)

    return ""


def get_date(iso_datetime: str | None) -> str:
    """
    Преобразует ISO8601 дату 'YYYY-MM-DDTHH:MM:SS.ssssss' в человекочитаемый формат 'DD.MM.YYYY'.
    Некорректные/пустые входы → пустая строка.
    """
    if not iso_datetime:
        return ""
    try:
        date_time_object = datetime.fromisoformat(iso_datetime)
        return date_time_object.strftime("%d.%m.%Y")
    except (ValueError, TypeError):
        return ""
