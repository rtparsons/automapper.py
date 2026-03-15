from typing import Any

import pytest
from pydantic import ValidationError

from automapper import mapper


def test_dict_to_pydantic_map(
    source_dict: dict,
    destination_pydantic: type,
) -> None:
    destination: Any = mapper.map(source_dict, destination_pydantic)

    assert destination.a == source_dict["a"]
    assert destination.b == source_dict["b"]
    assert isinstance(destination, destination_pydantic)


def test_dict_to_pydantic_map_missing_destination_field(
    source_dict: dict,
    destination_pydantic_with_less_fields: type,
) -> None:
    destination: Any = mapper.map(source_dict, destination_pydantic_with_less_fields)

    assert destination.a == source_dict["a"]
    assert not hasattr(destination, "b")
    assert isinstance(destination, destination_pydantic_with_less_fields)


def test_dict_to_pydantic_map_extra_destination_field_not_set(
    source_dict: dict,
    destination_pydantic_with_more_fields: type,
) -> None:
    with pytest.raises(ValidationError):
        mapper.map(source_dict, destination_pydantic_with_more_fields)


def test_dict_to_pydantic_map_extra_destination_field(
    source_dict: dict,
    destination_pydantic_with_more_fields: type,
) -> None:
    mapper.add(dict, destination_pydantic_with_more_fields, {"c": "b"})

    destination: Any = mapper.map(source_dict, destination_pydantic_with_more_fields)

    assert destination.a == source_dict["a"]
    assert destination.b == source_dict["b"]
    assert destination.c == source_dict["b"]
    assert isinstance(destination, destination_pydantic_with_more_fields)


def test_dict_to_pydantic_map_extra_field_via_function_mapping(
    source_dict: dict,
    destination_pydantic_with_more_fields: type,
) -> None:
    mapper.add(
        dict,
        destination_pydantic_with_more_fields,
        {"c": lambda src: src["b"].upper()},
    )

    destination: Any = mapper.map(source_dict, destination_pydantic_with_more_fields)

    assert destination.a == source_dict["a"]
    assert destination.b == source_dict["b"]
    assert destination.c == source_dict["b"].upper()
    assert isinstance(destination, destination_pydantic_with_more_fields)


def test_dict_to_pydantic_map_nonexistent_source_field(
    source_dict: dict,
    destination_pydantic: type,
) -> None:
    mapper.add(
        dict,
        destination_pydantic,
        {"c": "non_existent_field"},
    )

    with pytest.raises(AttributeError):
        mapper.map(source_dict, destination_pydantic)


def test_dict_to_pydantic_map_nonexistent_destination_field(
    source_dict: dict,
    destination_pydantic: type,
) -> None:
    mapper.add(
        dict,
        destination_pydantic,
        {"non_existent_field": "a"},
    )

    destination: Any = mapper.map(source_dict, destination_pydantic)
    assert not hasattr(destination, "non_existent_field")
