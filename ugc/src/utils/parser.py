from pymongo import DESCENDING, ASCENDING


def parse_sort(sort: str | None = None):
    if sort.startswith('-'):
        return {sort.removeprefix('-'): DESCENDING}

    return {sort: ASCENDING}
