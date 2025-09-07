import pytest

from automapper import mapper


@pytest.fixture(autouse=True)
def cleanup_mappings() -> None:
    mapper.clear_mappings()
