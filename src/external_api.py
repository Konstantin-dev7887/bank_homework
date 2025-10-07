from __future__ import annotations

import os
from typing import Any, Dict

import requests

API_URL = "https://api.apilayer.com/exchangerates_data/latest"
API_KEY = "EXCHANGE_RATES_API_KEY"
TARGET_CODE = "RUB"
SUPPORTED_CODES = ("USD", "EUR")


def convert_to_rub(transaction: Dict[str, Any]) -> float:
    """
    Возвращает сумму операции в рублях.
    - RUB -> просто float(amount)
    - USD/EUR -> запросить курс у API и умножить amount
    """
    try:
        operation = transaction["operationAmount"]
        amount_text = operation["amount"]
        code = operation["currency"]["code"]
    except Exception as exception:
        raise ValueError("Invalid transaction structure") from exception

    amount = float(str(amount_text).replace(",", "."))

    if code == TARGET_CODE:
        return amount

    if code not in SUPPORTED_CODES:
        return amount

    api_key = os.getenv(API_KEY)

    if not api_key:
        raise RuntimeError(f"Environment variable {API_KEY} is not set")

    rate = _fetch_rub_rate(base=code, api_key=api_key)
    return round(amount * rate, 2)


def _fetch_rub_rate(base: str, api_key: str) -> float:
    """
    Сходить в API за курсом base->RUB и вернуть курс.
    """
    headers = {"apikey": api_key}
    parameters = {"base": base, "symbols": TARGET_CODE}
    response = requests.get(API_URL,
                            headers=headers,
                            params=parameters,
                            timeout=10)
    response.raise_for_status()
    payload = response.json()
    rate = payload.get("rates", {}).get(TARGET_CODE)

    if rate is None:
        raise RuntimeError("RUB rate not found in API response")

    return float(rate)
