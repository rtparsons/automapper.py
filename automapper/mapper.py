from collections.abc import Callable
from typing import Any, TypeVar

S = TypeVar("S")
T = TypeVar("T")

_mappings: dict[tuple[type, type], dict[str, str | Callable]] = {}


def add(
    source: type[S],
    destination: type[T],
    mappings: dict[str, str | Callable],
) -> None:
    _mappings[(source, destination)] = mappings


def map(source: S, destination: type[T]) -> T:  # noqa: A001
    destination_props = _map_properties(source, destination)

    result: T = destination(**destination_props)

    return result


def clear_mappings() -> None:
    _mappings.clear()


def _source_to_dict(obj: S) -> dict[str, Any]:
    return {attr: getattr(obj, attr) for attr in dir(obj) if not attr.startswith("_")}


def _destination_properties(destination: type[T]) -> set[str]:
    return {
        field
        for field in vars(destination)["__dataclass_fields__"]
        if not field.startswith("_")
    }


def _apply_mappings(
    source: S,
    destination: type[T],
    source_props: dict[str, Any],
) -> None:
    mapping = _mappings.get((type(source), destination), {})
    for dest, src_mapper in mapping.items():
        if callable(src_mapper):
            source_props[dest] = src_mapper(source)
        else:
            source_props[dest] = source_props[src_mapper]


def _map_properties(source: S, destination: type[T]) -> dict[str, Any]:
    source_props = _source_to_dict(source)
    dest_props = _destination_properties(destination)

    _apply_mappings(source, destination, source_props)

    return {k: v for k, v in source_props.items() if k in dest_props}
