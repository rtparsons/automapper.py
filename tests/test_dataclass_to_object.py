from dataclasses import dataclass
from typing import Any

import pytest

from automapper import mapper


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


def test_dataclass_to_object_map(
    source_dataclass: type,
    destination_object: type,
) -> None:
    source = source_dataclass(a=1, b="test")
    destination: Any = mapper.map(source, destination_object)

    assert destination.a == source.a
    assert destination.b == source.b
    assert isinstance(destination, destination_object)


def test_dataclass_to_object_map_missing_destination_field(
    source_dataclass: type,
    destination_object_with_less_fields: type,
) -> None:
    source = source_dataclass(a=1, b="test")
    destination: Any = mapper.map(source, destination_object_with_less_fields)

    assert destination.a == source.a
    assert not hasattr(destination, "b")
    assert isinstance(destination, destination_object_with_less_fields)


def test_dataclass_to_object_map_extra_destination_field_not_set(
    source_dataclass: type,
    destination_object_with_more_fields: type,
) -> None:
    source = source_dataclass(a=1, b="test")

    with pytest.raises(TypeError):
        mapper.map(source, destination_object_with_more_fields)


def test_dataclass_to_object_map_extra_destination_field(
    source_dataclass: type,
    destination_object_with_more_fields: type,
) -> None:
    source = source_dataclass(a=1, b="test")
    mapper.add(source_dataclass, destination_object_with_more_fields, {"c": "b"})

    destination: Any = mapper.map(source, destination_object_with_more_fields)

    assert destination.a == source.a
    assert destination.b == source.b
    assert destination.c == source.b
    assert isinstance(destination, destination_object_with_more_fields)


def test_dataclass_to_object_map_extra_field_via_function_mapping(
    source_dataclass: type,
    destination_object_with_more_fields: type,
) -> None:
    source = source_dataclass(a=1, b="test")

    mapper.add(
        source_dataclass,
        destination_object_with_more_fields,
        {"c": lambda src: src.b.upper()},
    )

    destination: Any = mapper.map(source, destination_object_with_more_fields)

    assert destination.a == source.a
    assert destination.b == source.b
    assert destination.c == source.b.upper()
    assert isinstance(destination, destination_object_with_more_fields)


def test_dataclass_to_object_map_nonexistent_source_field(
    source_dataclass: type,
    destination_object: type,
) -> None:
    source = source_dataclass(a=1, b="test")

    mapper.add(
        source_dataclass,
        destination_object,
        {"c": "non_existent_field"},
    )

    with pytest.raises(AttributeError):
        mapper.map(source, destination_object)


def test_dataclass_to_object_map_nonexistent_destination_field(
    source_dataclass: type,
    destination_object: type,
) -> None:
    source = source_dataclass(a=1, b="test")

    mapper.add(
        source_dataclass,
        destination_object,
        {"non_existent_field": "a"},
    )

    destination: Any = mapper.map(source, destination_object)
    assert not hasattr(destination, "non_existent_field")
