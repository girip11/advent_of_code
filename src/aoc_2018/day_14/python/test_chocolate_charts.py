from pathlib import Path

from aoc_2018.day_14.python.chocolate_charts import (
    Elf,
    build_recipe_scoreboard,
    count_recipes_before_pattern,
)


def test_build_recipe_scoreboard() -> None:
    count = int((Path(__file__).parents[1] / "simple_input.txt").read_text())
    recipes = build_recipe_scoreboard([3, 7], count + 10, [Elf(0, 3), Elf(1, 7)])
    assert "".join(map(str, recipes[count : count + 10])) == "5941429882"


def test_count_recipes_before_pattern() -> None:
    recipe_count = count_recipes_before_pattern([3, 7], "01245", [Elf(0, 3), Elf(1, 7)])
    assert recipe_count == 5
