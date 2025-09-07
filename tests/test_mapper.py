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


def test_can_import() -> None:
    assert mapper is not None


def test_mapper_clear() -> None:
    mapper.add(int, str, {"value": "value"})
    assert mapper._mappings
    mapper.clear_mappings()
    assert not mapper._mappings


def test_dataclass_map(
    source_dataclass: type,
    destination_dataclass: type,
) -> None:
    source = source_dataclass(a=1, b="test")
    destination: Any = mapper.map(source, destination_dataclass)

    assert destination.a == source.a
    assert destination.b == source.b
    assert isinstance(destination, destination_dataclass)


def test_dataclass_map_missing_destination_field(
    source_dataclass: type,
    destination_dataclass_with_less_fields: type,
) -> None:
    source = source_dataclass(a=1, b="test")
    destination: Any = mapper.map(source, destination_dataclass_with_less_fields)

    assert destination.a == source.a
    assert not hasattr(destination, "b")
    assert isinstance(destination, destination_dataclass_with_less_fields)


def test_dataclass_map_extra_destination_field_not_set(
    source_dataclass: type,
    destination_dataclass_with_more_fields: type,
) -> None:
    source = source_dataclass(a=1, b="test")

    with pytest.raises(TypeError):
        mapper.map(source, destination_dataclass_with_more_fields)


def test_dataclass_map_extra_destination_field(
    source_dataclass: type,
    destination_dataclass_with_more_fields: type,
) -> None:
    source = source_dataclass(a=1, b="test")
    mapper.add(source_dataclass, destination_dataclass_with_more_fields, {"c": "b"})

    destination: Any = mapper.map(source, destination_dataclass_with_more_fields)

    assert destination.a == source.a
    assert destination.b == source.b
    assert destination.c == source.b
    assert isinstance(destination, destination_dataclass_with_more_fields)


def test_dataclass_map_extra_field_via_funcion_mapping(
    source_dataclass: type,
    destination_dataclass_with_more_fields: type,
) -> None:
    source = source_dataclass(a=1, b="test")

    mapper.add(
        source_dataclass,
        destination_dataclass_with_more_fields,
        {"c": lambda src: src.b.upper()},
    )

    destination: Any = mapper.map(source, destination_dataclass_with_more_fields)

    assert destination.a == source.a
    assert destination.b == source.b
    assert destination.c == source.b.upper()
    assert isinstance(destination, destination_dataclass_with_more_fields)
