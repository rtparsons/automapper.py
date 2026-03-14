# automapper

[![Python Version](https://img.shields.io/pypi/pyversions/automapper)](https://pypi.org/project/automapper/)
[![Tests](https://github.com/robprato/automapper.py/actions/workflows/test.yml/badge.svg)](https://github.com/robprato/automapper.py/actions/workflows/test.yml)

Simple Python object to dataclass mapper.

## Installation

```bash
pip install automapper
```

Or with Poetry:

```bash
poetry add automapper
```

## Basic Usage

Map a source object to a destination dataclass with matching property names:

```python
from dataclasses import dataclass
from automapper import mapper


@dataclass
class PersonDTO:
    name: str
    age: int


class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age


source = Person(name="John", age=30)
result = mapper.map(source, PersonDTO)

print(result)  # PersonDTO(name='John', age=30)
```

## Custom Mappings

### Property Renaming

Map source properties to differently-named destination properties:

```python
from dataclasses import dataclass
from automapper import mapper


@dataclass
class PersonDTO:
    full_name: str
    user_age: int


class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age


mapper.add(Person, PersonDTO, {
    "full_name": "name",
    "user_age": "age",
})

source = Person(name="John", age=30)
result = mapper.map(source, PersonDTO)

print(result)  # PersonDTO(full_name='John', user_age=30)
```

### Value Transformation

Use callables to transform values during mapping:

```python
from dataclasses import dataclass
from automapper import mapper


@dataclass
class PersonDTO:
    name: str
    age: int
    is_adult: bool


class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age


mapper.add(Person, PersonDTO, {
    "is_adult": lambda src: src.age >= 18,
})

source = Person(name="John", age=30)
result = mapper.map(source, PersonDTO)

print(result)  # PersonDTO(name='John', age=30, is_adult=True)
```

## API

### `mapper.add(source: type[S], destination: type[T], mappings: dict[str, str | Callable])`

Register a custom mapping between source and destination types.

### `mapper.map(source: S, destination: type[T]) -> T`

Map a source object to an instance of the destination dataclass.

### `mapper.clear_mappings()`

Clear all registered mappings.

## Development

```bash
# Install dependencies
poetry install

# Run tests
poetry run pytest

# Run linters
poetry run ruff check .
poetry run mypy .
```
