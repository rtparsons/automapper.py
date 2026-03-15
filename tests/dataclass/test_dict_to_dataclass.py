from typing import Any

import pytest

from automapper import mapper


def test_dict_to_dataclass_map(
    source_dict: dict,
    destination_dataclass: type,
) -> None:
    destination: Any = mapper.map(source_dict, destination_dataclass)

    assert destination.a == source_dict["a"]
    assert destination.b == source_dict["b"]
    assert isinstance(destination, destination_dataclass)


def test_dict_to_dataclass_map_missing_destination_field(
    source_dict: dict,
    destination_dataclass_with_less_fields: type,
) -> None:
    destination: Any = mapper.map(source_dict, destination_dataclass_with_less_fields)

    assert destination.a == source_dict["a"]
    assert not hasattr(destination, "b")
    assert isinstance(destination, destination_dataclass_with_less_fields)


def test_dict_to_dataclass_map_extra_destination_field_not_set(
    source_dict: dict,
    destination_dataclass_with_more_fields: type,
) -> None:
    with pytest.raises(TypeError):
        mapper.map(source_dict, destination_dataclass_with_more_fields)


def test_dict_to_dataclass_map_extra_destination_field(
    source_dict: dict,
    destination_dataclass_with_more_fields: type,
) -> None:
    mapper.add(dict, destination_dataclass_with_more_fields, {"c": "b"})

    destination: Any = mapper.map(source_dict, destination_dataclass_with_more_fields)

    assert destination.a == source_dict["a"]
    assert destination.b == source_dict["b"]
    assert destination.c == source_dict["b"]
    assert isinstance(destination, destination_dataclass_with_more_fields)


def test_dict_to_dataclass_map_extra_field_via_function_mapping(
    source_dict: dict,
    destination_dataclass_with_more_fields: type,
) -> None:
    mapper.add(
        dict,
        destination_dataclass_with_more_fields,
        {"c": lambda src: src["b"].upper()},
    )

    destination: Any = mapper.map(source_dict, destination_dataclass_with_more_fields)

    assert destination.a == source_dict["a"]
    assert destination.b == source_dict["b"]
    assert destination.c == source_dict["b"].upper()
    assert isinstance(destination, destination_dataclass_with_more_fields)


def test_dict_to_dataclass_map_nonexistent_source_field(
    source_dict: dict,
    destination_dataclass: type,
) -> None:
    mapper.add(
        dict,
        destination_dataclass,
        {"c": "non_existent_field"},
    )

    with pytest.raises(AttributeError):
        mapper.map(source_dict, destination_dataclass)


def test_dict_to_dataclass_map_nonexistent_destination_field(
    source_dict: dict,
    destination_dataclass: type,
) -> None:
    mapper.add(
        dict,
        destination_dataclass,
        {"non_existent_field": "a"},
    )

    destination: Any = mapper.map(source_dict, destination_dataclass)
    assert not hasattr(destination, "non_existent_field")
