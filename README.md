# Advent of code puzzles

Solutions to puzzles published at [adventofcode.com](https://adventofcode.com/)

## Python setup

* Prerequisites
  * Python 3.8.0 installed using **pyenv** -> `pyenv install 3.8.0`
  * **Pipenv** for managing dependencies.

* Editor of choice: VSCode

* Clone this repo and execute `pipenv --python 3.8.0 install --dev`. This sets up the virtual environment and installs dev dependencies like formatter (black), linter and ipython

* VSCode workspace configuration

```JSON
{
    "python.pythonPath": "/home/girish/.local/share/virtualenvs/advent_of_code-BswtnA1z/bin/python",
    "python.venvPath": "/home/girish/.local/share/virtualenvs",
    "python.pipenvPath": "/home/girish/.pyenv/shims/pipenv",
    "python.formatting.provider": "black",
    "python.formatting.blackArgs": ["-t", "py38", "-l", "100"],
    "python.linting.pylintEnabled": true,
    "python.linting.mypyEnabled": true,
    "python.linting.mypyArgs": [
      "--ignore-missing-imports",
      "--follow-imports=silent",
      "--show-column-numbers"
    ],
    "python.linting.enabled": true,
    "python.linting.lintOnSave": true,
    "python.autoComplete.showAdvancedMembers": true,
    "python.testing.unittestEnabled": false,
    "python.testing.nosetestsEnabled": false,
    "python.testing.pytestEnabled": true,
    "python.testing.pytestPath": "pytest"
}
```

## Github actions locally

```bash
act pull_request -W .github/workflows/
```

---

## Reference

* [Running github actions locally](https://github.com/nektos/act)
