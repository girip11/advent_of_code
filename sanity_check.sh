#!/bin/bash

set -eu

function run_tools() {
  pattern="$1"
  echo "Running black"
  pipenv run black -t py38 -l 100 --check "$pattern"
  echo "Running isort"
  pipenv run isort --py 38 --check "$pattern"
  echo "Running pylint"
  pipenv run pylint "$pattern"
  echo "Running flake8"
  pipenv run flake8 "$pattern"
  echo "Running mypy"
  pipenv run mypy "$pattern"
  echo "Running pytest"
  pipenv run pytest "$pattern"
}

pattern="${1:-aoc_*}"
echo "$pattern"
run_tools "$pattern"
