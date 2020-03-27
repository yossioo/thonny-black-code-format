function Dependencies {
    python -m pip install --upgrade pip

    pip install black
    pip install coverage
    pip install thonny

}

function Tests {
    coverage run --source=thonnycontrib -m unittest
    coverage report --show-missing
}
