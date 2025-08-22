from src.processing import filter_by_state, sort_by_date

def test_filter_by_state_default():
    operations = [
        {"id": 1, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 2, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 3, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    ]
    filtered_operations = filter_by_state(operations)
    assert [operation["id"] for operation in filtered_operations] == [1, 2]

def test_sort_by_date_desc():
    operations = [
        {"id": 1, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 2, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 3, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    ]
    sorted_operations = sort_by_date(operations)
    assert [operation["id"] for operation in sorted_operations] == [1, 3, 2]