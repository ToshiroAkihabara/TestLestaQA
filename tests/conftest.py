from engine2D import Engine2D
import pytest

@pytest.fixture
def engine():
    engine = Engine2D()
    return engine