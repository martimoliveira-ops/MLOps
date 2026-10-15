.PHONY: install format format-check lint test test-ci all

SRC = src
TESTS = tests

install:
	python -m pip install --upgrade pip
	python -m pip install -r requirements.txt
	python -m pip install -r requirements-dev.txt
	python -m pip install -e .

format:
	python -m black $(SRC) $(TESTS)

format-check:
	python -m black --check $(SRC) $(TESTS)

lint:
	python -m pylint --recursive=y --disable=R,C $(SRC) $(TESTS)

test:
	python -m pytest -vv --cov=forecaster $(TESTS)

test-ci:
	python -m pytest -vv --cov=forecaster --junitxml=test-results.xml $(TESTS)

all: install format lint test
