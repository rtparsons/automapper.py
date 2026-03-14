from automapper import mapper


def test_can_import() -> None:
    assert mapper is not None


def test_mapper_clear() -> None:
    mapper.add(int, str, {"value": "value"})
    assert mapper._mappings
    mapper.clear_mappings()
    assert not mapper._mappings
