#!/bin/sh

linter_dependencies()
{
  python -m pip install --upgrade pip

  pip install flake8
  pip install black
}

lint()
{
  python -m flake8 . --count --select=E9,F63,F7,F82 --exclude=./tests/with_errors.py --show-source --statistics
  python -m flake8 . --count --exclude=./tests/with_errors.py --exit-zero --max-complexity=10 --max-line-length=88 --statistics
}

black_format()
{
  black . --check --exclude="(with_errors|successful)\.py"
}


tests_dependencies()
{
  python -m pip install --upgrade pip

  pip install black
  pip install coverage
  pip install thonny
}

tests()
{
  coverage run --source=thonnycontrib -m unittest
  coverage report --show-missing
}
