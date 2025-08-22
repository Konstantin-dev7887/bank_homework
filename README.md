Виджет банковских операций
==========================

Проект для обработки и маскирования банковских операций:
- фильтрация по статусу,
- сортировка по дате,
- маскирование карт и счетов.

Установка и настройка окружения
--------------------------------
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows

(при использовании poetry можно poetry install)

Использование
--------------
Пример работы с модулем processing:

    from src.processing import filter_by_state, sort_by_date

    operations = [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED",  "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED",  "date": "2018-10-14T08:21:33.419441"}
    ]

    print(filter_by_state(operations))
    print(sort_by_date(operations, reverse=True))

Пример работы с модулем masks:

    from src.masks import get_mask_card_number, get_mask_account

    print(get_mask_card_number("4111 1111 1111 1111"))   # -> 4111 11** **** 1111
    print(get_mask_account("Счет 12345678901234567890")) # -> Счет **7890

Пример работы с модулем widget:

    from src.widget import mask_account_card, get_date

    print(mask_account_card("Visa Classic 4111 1111 1111 1111")) # -> Visa Classic 4111 11** **** 1111
    print(get_date("2019-07-03T18:35:29.512364"))                # -> 03.07.2019

Тестирование
-------------
Для запуска тестов используется pytest:

    pytest

Проверка покрытия тестами:

    pytest --cov=src --cov-report=term-missing --cov-report=html:coverage_html

После выполнения появится HTML-отчёт в папке coverage_html/ (открыть index.html в браузере).

Линтеры и форматтеры
---------------------
Перед коммитом рекомендуется проверять код:

    flake8 src tests
    mypy src
    isort src

GitFlow
--------
Разработка ведётся по GitFlow:
- основная ветка - main
- рабочая ветка - develop
- домашние задания выполняются в ветках feature/