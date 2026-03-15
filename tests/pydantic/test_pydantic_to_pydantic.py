from typing import Any

import pytest
from pydantic import ValidationError

from automapper import mapper


def test_pydantic_map(
    source_pydantic: type,
    destination_pydantic: type,
) -> None:
    source = source_pydantic(a=1, b="test")
    destination: Any = mapper.map(source, destination_pydantic)

    assert destination.a == source.a
    assert destination.b == source.b
    assert isinstance(destination, destination_pydantic)


def test_pydantic_map_missing_destination_field(
    source_pydantic: type,
    destination_pydantic_with_less_fields: type,
) -> None:
    source = source_pydantic(a=1, b="test")
    destination: Any = mapper.map(source, destination_pydantic_with_less_fields)

    assert destination.a == source.a
    assert not hasattr(destination, "b")
    assert isinstance(destination, destination_pydantic_with_less_fields)


def test_pydantic_map_extra_destination_field_not_set(
    source_pydantic: type,
    destination_pydantic_with_more_fields: type,
) -> None:
    source = source_pydantic(a=1, b="test")

    with pytest.raises(ValidationError):
        mapper.map(source, destination_pydantic_with_more_fields)


def test_pydantic_map_extra_destination_field(
    source_pydantic: type,
    destination_pydantic_with_more_fields: type,
) -> None:
    source = source_pydantic(a=1, b="test")
    mapper.add(source_pydantic, destination_pydantic_with_more_fields, {"c": "b"})

    destination: Any = mapper.map(source, destination_pydantic_with_more_fields)

    assert destination.a == source.a
    assert destination.b == source.b
    assert destination.c == source.b
    assert isinstance(destination, destination_pydantic_with_more_fields)


def test_pydantic_map_extra_field_via_function_mapping(
    source_pydantic: type,
    destination_pydantic_with_more_fields: type,
) -> None:
    source = source_pydantic(a=1, b="test")

    mapper.add(
        source_pydantic,
        destination_pydantic_with_more_fields,
        {"c": lambda src: src.b.upper()},
    )

    destination: Any = mapper.map(source, destination_pydantic_with_more_fields)

    assert destination.a == source.a
    assert destination.b == source.b
    assert destination.c == source.b.upper()
    assert isinstance(destination, destination_pydantic_with_more_fields)


def test_pydantic_map_nonexistent_source_field(
    source_pydantic: type,
    destination_pydantic: type,
) -> None:
    source = source_pydantic(a=1, b="test")

    mapper.add(
        source_pydantic,
        destination_pydantic,
        {"c": "non_existent_field"},
    )

    with pytest.raises(AttributeError):
        mapper.map(source, destination_pydantic)


def test_pydantic_map_nonexistent_destination_field(
    source_pydantic: type,
    destination_pydantic: type,
) -> None:
    source = source_pydantic(a=1, b="test")

    mapper.add(
        source_pydantic,
        destination_pydantic,
        {"non_existent_field": "a"},
    )

    destination: Any = mapper.map(source, destination_pydantic)
    assert not hasattr(destination, "non_existent_field")
