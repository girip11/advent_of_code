# I do need to maintain each cart's position and what turn it will take at intersection

import sys
from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Elf:
    position: int
    score: int


def _build_new_recipes(elves: List[Elf]) -> List[int]:
    score = sum(map(lambda elf: elf.score, elves))

    if score < 10:
        return [score]

    return [score // 10, score % 10]


# keep it simple initially
def _select_next_recipe(current_recipes: List[int], elf: Elf) -> Elf:
    recipes = len(current_recipes)
    new_position = ((elf.score + 1) - (recipes - elf.position)) % recipes

    return Elf(new_position, current_recipes[new_position])


def build_recipe_scoreboard(
    current_recipes: List[int], recipes: int, elves: List[Elf]
) -> List[int]:

    for _ in range(recipes):
        current_recipes.extend(_build_new_recipes(elves))

        # choose next recipe
        elves = [_select_next_recipe(current_recipes, elf) for elf in elves]

    return current_recipes


def count_recipes_before_pattern(current_recipes: List[int], pattern: str, elves: List[Elf]) -> int:

    pattern_loc = -1
    pattern_len = len(pattern)

    while True:
        new_recipes = _build_new_recipes(elves)
        current_recipes.extend(new_recipes)

        recipes = len(current_recipes)

        if recipes >= (pattern_len + 1):
            recent_pattern = "".join(map(str, current_recipes[-(pattern_len + 1) :]))

            if (loc := recent_pattern.find(pattern)) != -1:
                pattern_loc = recipes - (pattern_len + 1) + loc
                break

        # choose next recipe
        elves = [_select_next_recipe(current_recipes, elf) for elf in elves]

    return pattern_loc


def main(_: List[str]) -> None:
    input_ = (sys.stdin.readline()).strip()
    recipes_to_complete = int(input_)

    current_recipes = [3, 7]
    elf1 = Elf(0, current_recipes[0])
    elf2 = Elf(1, current_recipes[1])

    # part-1
    recipe_scores = build_recipe_scoreboard(
        current_recipes.copy(), recipes_to_complete + 10, [elf1, elf2]
    )
    print("".join(map(str, recipe_scores[recipes_to_complete : recipes_to_complete + 10])))

    # part-2
    pattern = input_
    recipes_count = count_recipes_before_pattern(current_recipes.copy(), pattern, [elf1, elf2])
    print(recipes_count)


if __name__ == "__main__":
    main(sys.argv)
