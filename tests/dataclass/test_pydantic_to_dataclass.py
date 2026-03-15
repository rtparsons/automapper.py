from typing import Any

import pytest

from automapper import mapper


def test_pydantic_to_dataclass_map(
    source_pydantic: type,
    destination_dataclass: type,
) -> None:
    source = source_pydantic(a=1, b="test")
    destination: Any = mapper.map(source, destination_dataclass)

    assert destination.a == source.a
    assert destination.b == source.b
    assert isinstance(destination, destination_dataclass)


def test_pydantic_to_dataclass_map_missing_destination_field(
    source_pydantic: type,
    destination_dataclass_with_less_fields: type,
) -> None:
    source = source_pydantic(a=1, b="test")
    destination: Any = mapper.map(source, destination_dataclass_with_less_fields)

    assert destination.a == source.a
    assert not hasattr(destination, "b")
    assert isinstance(destination, destination_dataclass_with_less_fields)


def test_pydantic_to_dataclass_map_extra_destination_field_not_set(
    source_pydantic: type,
    destination_dataclass_with_more_fields: type,
) -> None:
    source = source_pydantic(a=1, b="test")

    with pytest.raises(TypeError):
        mapper.map(source, destination_dataclass_with_more_fields)


def test_pydantic_to_dataclass_map_extra_destination_field(
    source_pydantic: type,
    destination_dataclass_with_more_fields: type,
) -> None:
    source = source_pydantic(a=1, b="test")
    mapper.add(source_pydantic, destination_dataclass_with_more_fields, {"c": "b"})

    destination: Any = mapper.map(source, destination_dataclass_with_more_fields)

    assert destination.a == source.a
    assert destination.b == source.b
    assert destination.c == source.b
    assert isinstance(destination, destination_dataclass_with_more_fields)


def test_pydantic_to_dataclass_map_extra_field_via_function_mapping(
    source_pydantic: type,
    destination_dataclass_with_more_fields: type,
) -> None:
    source = source_pydantic(a=1, b="test")

    mapper.add(
        source_pydantic,
        destination_dataclass_with_more_fields,
        {"c": lambda src: src.b.upper()},
    )

    destination: Any = mapper.map(source, destination_dataclass_with_more_fields)

    assert destination.a == source.a
    assert destination.b == source.b
    assert destination.c == source.b.upper()
    assert isinstance(destination, destination_dataclass_with_more_fields)


def test_pydantic_to_dataclass_map_nonexistent_source_field(
    source_pydantic: type,
    destination_dataclass: type,
) -> None:
    source = source_pydantic(a=1, b="test")

    mapper.add(
        source_pydantic,
        destination_dataclass,
        {"c": "non_existent_field"},
    )

    with pytest.raises(AttributeError):
        mapper.map(source, destination_dataclass)


def test_pydantic_to_dataclass_map_nonexistent_destination_field(
    source_pydantic: type,
    destination_dataclass: type,
) -> None:
    source = source_pydantic(a=1, b="test")

    mapper.add(
        source_pydantic,
        destination_dataclass,
        {"non_existent_field": "a"},
    )

    destination: Any = mapper.map(source, destination_dataclass)
    assert not hasattr(destination, "non_existent_field")
