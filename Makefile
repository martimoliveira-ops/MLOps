.PHONY: install format format-check lint test all

install:
	python -m pip install --upgrade pip
	python -m pip install -r requirements.txt

format:
	python -m black chain_of_functions.py test_chain_function.py

format-check:
	python -m black --check chain_of_functions.py test_chain_function.py

lint:
	python -m pylint --disable=R,C chain_of_functions.py test_chain_function.py

test:
	python -m pytest -vv --cov=chain_of_functions test_chain_function.py

all: install format lint test
