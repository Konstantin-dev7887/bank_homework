import pytest
from src.widget import mask_account_card, get_date


@pytest.mark.parametrize("account_card, account_card_mask", [
    ("Visa Classic 4111 1111 1111 1111", "Visa Classic 4111 11** **** 1111"),
    ("Счет 12345678901234567890", "Счет **7890"),
    ("", ""),
    (None, ""),
])
def test_mask_account_card(account_card: str | None, account_card_mask: str) -> None:
    assert mask_account_card(account_card) == account_card_mask


@pytest.mark.parametrize("date_time_object, expected_date", [
    ("2019-07-03T18:35:29.512364", "03.07.2019"),
    ("2018-06-30T02:08:58.425572", "30.06.2018"),
    ("wrong-date", ""),
    ("", ""),
])
def test_get_date(date_time_object: str, expected_date: str) -> None:
    assert get_date(date_time_object) == expected_date
