.PHONY: install install-train format format-check lint test test-ci run all

SRC = src
TESTS = tests

install:
	python -m pip install --upgrade pip
	python -m pip install -r requirements.txt
	python -m pip install -r requirements-dev.txt
	python -m pip install -e .

install-train:
	python -m pip install -r requirements-train.txt

format:
	python -m black $(SRC) $(TESTS)

format-check:
	python -m black --check $(SRC) $(TESTS)

lint:
	python -m pylint $(SRC) $(TESTS)

test:
	python -m pytest -vv --cov=forecaster $(TESTS)

test-ci:
	python -m pytest -vv --cov=forecaster --junitxml=test-results.xml $(TESTS)

run:
	python -m uvicorn forecaster.api:app --reload

all: install format lint test
