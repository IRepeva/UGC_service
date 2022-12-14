from pymongo import DESCENDING, ASCENDING


def parse_sort(sort: str):
    if sort.startswith('-'):
        return {sort.removeprefix('-'): DESCENDING}

    return {sort: ASCENDING}
