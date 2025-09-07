build:
	poetry install

lint:
	poetry run ruff check .
	poetry run mypy .

format:
	poetry run ruff check . --fix
	poetry run ruff format .

test:
	poetry run coverage run --source automapper -m pytest
	poetry run coverage report -m
