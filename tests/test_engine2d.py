from engine2D import Engine2D
import pytest 
from contextlib import nullcontext as does_not_raises

@pytest.fixture
def clear_canvas(engine: Engine2D):
    engine.clear_canvas()

@pytest.fixture
def get_random_color(engine: Engine2D):
    engine.change_color_pencil()
    color = engine.show_color_pencil()
    return color

@pytest.fixture
def circle(engine: Engine2D):
    circle = engine.get_circle()
    return circle

class TestEngine2D:
    def test_pattern_singleton(self, engine: Engine2D):
        engine = engine
        engine2 = engine
        assert id(engine) == id(engine2)

    def test_empty_canvas(self, engine: Engine2D):
        assert engine.show_canvas() == []
    
    def test_clear_canvas(self, engine: Engine2D):
        engine.add_circle()
        engine.clear_canvas()
        engine.show_canvas()
        assert engine.show_canvas() == []

    def test_get_color_pencil(self, engine: Engine2D):
        assert engine.show_color_pencil() == "Black"

    def test_change_color_pencil(self, engine: Engine2D, get_random_color):
        new_color = get_random_color
        assert engine.show_color_pencil() == new_color

@pytest.mark.usefixtures("clear_canvas")
class TestCanvas:
    def test_add_circle(self, engine: Engine2D):
        engine.add_circle()
        assert engine.show_canvas() == ["Circle"]

    def test_add_triangle(self, engine: Engine2D):
        engine.add_triangle()
        assert engine.show_canvas() == ["Triangle"]

    def test_add_rectangle(self, engine: Engine2D):
        engine.add_rectangle()
        assert engine.show_canvas() == ["Rectangle"]

    def test_add_some_figures(self, engine: Engine2D):
        engine.add_circle()
        engine.add_triangle()
        engine.add_rectangle()
        assert engine.show_canvas() == ["Circle", "Triangle", "Rectangle"]

class TestCircle:
    @pytest.mark.parametrize(
    "test_radius, expected_result, expectation", 
    [
        (5, 10, does_not_raises()),
        (10, 20, does_not_raises()),
        (0, 0, does_not_raises()),
        (-4, 8, does_not_raises()),
        (2.5, 5, does_not_raises()),
        ("7", 14, pytest.raises(TypeError))
    ]
    )
    def test_circle(self, engine: Engine2D, test_radius, expected_result, expectation):
        with expectation:
            circle = engine.get_circle(color="Black", radius=test_radius)
            assert circle._diameter == expected_result
