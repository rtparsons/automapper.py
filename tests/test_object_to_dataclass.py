from dataclasses import dataclass
from typing import Any

import pytest

from automapper import mapper


class Source:
    def __init__(self, a: int, b: str) -> None:
        self.a = a
        self.b = b


@pytest.fixture
def source_object() -> type:
    return Source


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


def test_object_map(
    source_object: type,
    destination_dataclass: type,
) -> None:
    source = source_object(a=1, b="test")
    destination: Any = mapper.map(source, destination_dataclass)

    assert destination.a == source.a
    assert destination.b == source.b
    assert isinstance(destination, destination_dataclass)


def test_object_map_missing_destination_field(
    source_object: type,
    destination_dataclass_with_less_fields: type,
) -> None:
    source = source_object(a=1, b="test")
    destination: Any = mapper.map(source, destination_dataclass_with_less_fields)

    assert destination.a == source.a
    assert not hasattr(destination, "b")
    assert isinstance(destination, destination_dataclass_with_less_fields)


def test_object_map_extra_destination_field_not_set(
    source_object: type,
    destination_dataclass_with_more_fields: type,
) -> None:
    source = source_object(a=1, b="test")

    with pytest.raises(TypeError):
        mapper.map(source, destination_dataclass_with_more_fields)


def test_object_map_extra_destination_field(
    source_object: type,
    destination_dataclass_with_more_fields: type,
) -> None:
    source = source_object(a=1, b="test")
    mapper.add(source_object, destination_dataclass_with_more_fields, {"c": "b"})

    destination: Any = mapper.map(source, destination_dataclass_with_more_fields)

    assert destination.a == source.a
    assert destination.b == source.b
    assert destination.c == source.b
    assert isinstance(destination, destination_dataclass_with_more_fields)


def test_object_map_extra_field_via_funcion_mapping(
    source_object: type,
    destination_dataclass_with_more_fields: type,
) -> None:
    source = source_object(a=1, b="test")

    mapper.add(
        source_object,
        destination_dataclass_with_more_fields,
        {"c": lambda src: src.b.upper()},
    )

    destination: Any = mapper.map(source, destination_dataclass_with_more_fields)

    assert destination.a == source.a
    assert destination.b == source.b
    assert destination.c == source.b.upper()
    assert isinstance(destination, destination_dataclass_with_more_fields)


def test_object_map_nonexistent_source_field(
    source_object: type,
    destination_dataclass: type,
) -> None:
    source = source_object(a=1, b="test")

    mapper.add(
        source_object,
        destination_dataclass,
        {"c": "non_existent_field"},
    )

    with pytest.raises(AttributeError):
        mapper.map(source, destination_dataclass)


def test_object_map_nonexistent_destination_field(
    source_object: type,
    destination_dataclass: type,
) -> None:
    source = source_object(a=1, b="test")

    mapper.add(
        source_object,
        destination_dataclass,
        {"non_existent_field": "a"},
    )

    destination: Any = mapper.map(source, destination_dataclass)
    assert not hasattr(destination, "non_existent_field")
