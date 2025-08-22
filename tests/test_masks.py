from __future__ import annotations

import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.mark.parametrize(
    "card_number, expected_card_number_mask",
    [
        ("5555444433331111", "5555 44** **** 1111"),
        ("4111 1111 1111 1111", "4111 11** **** 1111"),
        ("", ""),
        ("123", ""),
    ],
)
def test_get_mask_card_number(card_number: str, expected_card_number_mask: str) -> None:
    assert get_mask_card_number(card_number) == expected_card_number_mask


@pytest.mark.parametrize(
    "account, expected_account_mask",
    [
        ("Счет 12345678901234567890", "Счет **7890"),
        ("Счёт 00001234", "Счёт **1234"),
        ("1234", "**1234"),
        ("12", ""),
    ],
)
def test_get_mask_account(account, expected_account_mask) -> None:
    assert get_mask_account(account) == expected_account_mask
