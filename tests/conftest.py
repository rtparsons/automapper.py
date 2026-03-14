from collections.abc import Generator
from dataclasses import dataclass

import pytest

from automapper import mapper


class SourceObject:
    def __init__(self, a: int, b: str) -> None:
        self.a = a
        self.b = b


@pytest.fixture
def source_dict() -> dict:
    return {"a": 1, "b": "test"}


@pytest.fixture
def source_object() -> type:
    return SourceObject


@pytest.fixture
def source_dataclass() -> type:
    @dataclass
    class Source:
        a: int
        b: str

    return Source


@pytest.fixture
def destination_object() -> type:
    class Destination:
        def __init__(self, a: int, b: str) -> None:
            self.a = a
            self.b = b

    return Destination


@pytest.fixture
def destination_object_with_less_fields() -> type:
    class DestinationLessFields:
        def __init__(self, a: int) -> None:
            self.a = a

    return DestinationLessFields


@pytest.fixture
def destination_object_with_more_fields() -> type:
    class DestinationMoreFields:
        def __init__(self, a: int, b: str, c: str) -> None:
            self.a = a
            self.b = b
            self.c = c

    return DestinationMoreFields


@pytest.fixture
def destination_dataclass() -> type:
    @dataclass
    class Destination:
        a: int
        b: str

    return Destination


@pytest.fixture
def destination_dataclass_with_less_fields() -> type:
    @dataclass
    class DestinationLessFields:
        a: int

    return DestinationLessFields


@pytest.fixture
def destination_dataclass_with_more_fields() -> type:
    @dataclass
    class DestinationMoreFields:
        a: int
        b: str
        c: str

    return DestinationMoreFields


@pytest.fixture(autouse=True)
def cleanup_mappings() -> Generator[None, None, None]:
    yield
    mapper.clear_mappings()
