from __future__ import annotations

from datetime import datetime

from .masks import get_mask_account, get_mask_card_number

ACCOUNT_PREFIX_1: str = "Счет "
ACCOUNT_PREFIX_2: str = "Счёт "
CARD_BRANDS: tuple[str, ...] = ("visa", "mastercard", "maestro", "mir")
DATE_OUT_FMT: str = "%d.%m.%Y"


def mask_account_card(account_card: str | int | None) -> str:
    """
    Определяет тип входа и применяет нужную маску.
    Некорректные входы → пустая строка.
    """
    if account_card is None:
        return ""

    account_card_text = str(account_card).strip()

    if not account_card_text:
        return ""

    if (account_card_text.startswith(ACCOUNT_PREFIX_1) or
            account_card_text.startswith(ACCOUNT_PREFIX_2)):
        return get_mask_account(account_card_text)

    digits = _get_only_digits(account_card_text)

    if not digits:
        return ""

    lower_account_card = account_card_text.lower()

    is_card = (any(brand in lower_account_card for brand in CARD_BRANDS) or
               len(digits) >= 16)

    if is_card:
        masked_card_number = get_mask_card_number(account_card_text)

        first_digit_idx = next((i for i, symbol in enumerate(account_card_text)
                                if symbol.isdigit()), -1)

        if first_digit_idx > 0:
            prefix = account_card_text[:first_digit_idx].rstrip()
            return f"{prefix} {masked_card_number}".strip()

        return masked_card_number

    if len(digits) >= 10:
        return get_mask_account(account_card_text)

    return ""


def get_date(iso_datetime: str | None) -> str:
    """
    Преобразует ISO8601 дату 'YYYY-MM-DDTHH:MM:SS.ssssss'
    в человекочитаемый формат 'DD.MM.YYYY'.
    Некорректные/пустые входы → пустая строка.
    """
    if not iso_datetime:
        return ""
    try:
        date_time_object = datetime.fromisoformat(iso_datetime)
        return date_time_object.strftime("%d.%m.%Y")
    except (ValueError, TypeError):
        return ""


def _get_only_digits(text: str) -> str:
    return "".join(symbol for symbol in text if symbol.isdigit())
