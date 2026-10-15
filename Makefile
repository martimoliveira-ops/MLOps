.PHONY: install format format-check lint test test-ci all

SRC = chain_of_functions.py app.py
TESTS = test_chain_function.py test_app.py

install:
	python -m pip install --upgrade pip
	python -m pip install -r requirements.txt
	python -m pip install -r requirements-dev.txt

format:
	python -m black $(SRC) $(TESTS)

format-check:
	python -m black --check $(SRC) $(TESTS)

lint:
	python -m pylint --disable=R,C $(SRC) $(TESTS)

test:
	python -m pytest -vv --cov=chain_of_functions --cov=app $(TESTS)

test-ci:
	python -m pytest -vv --cov=chain_of_functions --cov=app --junitxml=test-results.xml $(TESTS)

all: install format lint test
