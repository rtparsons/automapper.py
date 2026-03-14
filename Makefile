build:
	poetry install

lint:
	poetry run ruff check .
	poetry run mypy .

format:
	poetry run ruff check . --fix
	poetry run ruff format .

test:
	poetry run nox
