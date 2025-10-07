from __future__ import annotations

from typing import Any, Dict, Iterable, List

from src.processing import filter_by_state, sort_by_date
from src.search import process_bank_search
from src.utils import (
    read_transactions_csv,
    read_transactions_excel,
    read_transactions_json,
)
from src.widget import get_date, mask_account_card

Transaction = Dict[str, Any]
ALLOWED_STATUSES = {"EXECUTED", "CANCELED", "PENDING"}


def _prompt_menu() -> int:
    print("Привет! "
          "Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    while True:
        operation_number = input("> ").strip()

        if operation_number in {"1", "2", "3"}:
            return int(operation_number)

        print("Пожалуйста, введите 1 / 2 / 3.")


def _load_data(choice: int) -> List[Transaction]:
    if choice == 1:
        print("Для обработки выбран JSON-файл.")
        path = input("Укажите путь к JSON-файлу "
                     "(например, data/operations.json): ").strip()
        return read_transactions_json(path)
    if choice == 2:
        print("Для обработки выбран CSV-файл.")
        path = input("Укажите путь к CSV-файлу "
                     "(например, data/transactions.csv): ").strip()
        return read_transactions_csv(path)

    print("Для обработки выбран XLSX-файл.")
    path = input("Укажите путь к XLSX-файлу "
                 "(например, data/transactions_excel.xlsx): ").strip()

    return read_transactions_excel(path)


def _prompt_status() -> str:
    print("Введите статус, по которому необходимо выполнить фильтрацию.")
    print("Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")

    while True:
        status = input("> ").strip().upper()

        if status in ALLOWED_STATUSES:
            print(f'Операции отфильтрованы по статусу "{status}"')
            return status

        print(f'Статус операции "{status}" недоступен.')


def _yes(prompt: str) -> bool:
    answer = input(f"{prompt} Да/Нет\n> ").strip().lower()
    return answer in {"да", "yes", "y", "д"}


def _print_transactions(items: Iterable[Transaction]) -> None:
    items = list(items)

    if not items:
        print("Не найдено ни одной транзакции, "
              "подходящей под ваши условия фильтрации")
        return

    print("Распечатываю итоговый список транзакций...")
    print(f"Всего банковских операций в выборке: {len(items)}\n")

    for transaction in items:
        date_out = (get_date(transaction.get("date"))
                    or "")
        description = (transaction.get("description")
                       or "")
        from_masked = mask_account_card(transaction.get("from"))
        to_masked = mask_account_card(transaction.get("to"))
        amount = ((transaction.get("operationAmount")
                   or {}).get("amount")
                  or "")
        currency_name = (((transaction.get("operationAmount")
                           or {}).get("currency")
                          or {}).get("name")
                         or "")

        print(f"{date_out} {description}")
        line = []

        if from_masked:
            line.append(from_masked)

        if to_masked:
            arrow = " -> " if line else ""
            line.append(f"{arrow}{to_masked}")

        if line:
            print("".join(line))

        print(f"Сумма: {amount} {currency_name}\n")


def main() -> None:
    choice = _prompt_menu()
    items = _load_data(choice)

    status = _prompt_status()
    items = filter_by_state(items, state=status)

    if _yes("Отсортировать операции по дате?"):
        ascending = _yes("Отсортировать по возрастанию?")
        items = sort_by_date(items, reverse=not ascending)

    if _yes("Выводить только рублевые транзакции?"):
        items = [
            transaction for transaction in items
            if ((transaction.get("operationAmount")
                 or {}).get("currency")
                or {}).get("code") == "RUB"
        ]

    if _yes("Отфильтровать список транзакций "
            "по определенному слову в описании?"):
        word = input("Введите слово/фразу для поиска: ").strip()

        if word:
            items = process_bank_search(items, word)

    _print_transactions(items)


if __name__ == "__main__":
    main()
