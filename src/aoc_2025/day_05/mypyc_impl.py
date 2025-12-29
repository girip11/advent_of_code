import bisect
from collections.abc import Iterator


class FreshIngredientsDB:
    def __init__(self) -> None:
        self.__ids_db: list[tuple[int, int]] = []

    @property
    def fresh_ingredients(self) -> list[tuple[int, int]]:
        return self.__ids_db

    def add_ingredient_ids(self, id_range: tuple[int, int]) -> None:
        bisect.insort_left(self.__ids_db, id_range)

    def consolidate_db(self) -> None:
        db = [self.__ids_db[0]]
        db_idx = 0

        for c_start, c_end in self.__ids_db[1:]:
            p_start, p_end = db[db_idx]

            if p_start <= c_start <= p_end:
                db.pop()
                db.append((p_start, max(p_end, c_end)))
            else:
                db.append((c_start, c_end))
                db_idx += 1

        self.__ids_db = db

    def is_ingredient_fresh(self, id_: int) -> bool:
        return id_ in self

    def __contains__(self, id_: int) -> bool:
        loc = bisect.bisect_left(self.__ids_db, id_, key=lambda e: e[0])
        return self.__ids_db[loc - 1][0] <= id_ <= self.__ids_db[loc - 1][1]
        # linear search
        # return any(start <= id_ <= end for start, end in self.__ids_db)

    def total_fresh_ingredients(self) -> int:
        return sum((end - start + 1) for start, end in self.__ids_db)


def parse_database(db: Iterator[str]) -> tuple[FreshIngredientsDB, list[int]]:
    fresh_ingredients = FreshIngredientsDB()
    avail_ingredients = []

    for line in map(str.strip, db):
        if len(line) == 0:
            break

        id_ranges = map(int, line.split("-"))
        fresh_ingredients.add_ingredient_ids((next(id_ranges), next(id_ranges)))

    fresh_ingredients.consolidate_db()

    for line in map(str.strip, db):
        if len(line) == 0:
            break
        avail_ingredients.append(int(line))

    return (fresh_ingredients, avail_ingredients)


def count_available_fresh_ingredients(db: Iterator[str]) -> tuple[int, int]:
    fresh_ingredients, avail_ingredients = parse_database(db)

    # part - 1
    available_fresh_ingredients = sum(
        1 for ingredient in avail_ingredients if ingredient in fresh_ingredients
    )

    # part-2
    total_fresh_ingredients = fresh_ingredients.total_fresh_ingredients()
    return (available_fresh_ingredients, total_fresh_ingredients)
