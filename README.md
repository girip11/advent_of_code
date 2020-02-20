# Advent of code puzzles

Solutions to puzzles published at [adventofcode.com](https://adventofcode.com/)

## Python setup

* Prerequisites
  * Python 3.8.0 installed using **pyenv** -> `pyenv install 3.8.0`
  * **Pipenv** for managing dependencies.

* Editor of choice: VSCode

* Clone this repo and execute `pipenv --python 3.8.0 install --dev`. This sets up the virtual environment and installs dev dependencies like formatter (black), linter and ipython

* After installing all the dev dependencies, for the **mypy** vscode extension to work, install the **mypyls** (MyPy Language server) in to the pipenv provided virtual environment.

```bash
pipenv shell
pip install "https://github.com/matangover/mypyls/archive/master.zip#egg=mypyls[default-mypy]"
```

**NOTE**: If you update the mypy-vscode extension, you may also need to update the mypy language server separately. Do so by running the following command.

```Bash
pip install -U "https://github.com/matangover/mypyls/archive/master.zip#egg=mypyls[default-mypy]"
```
