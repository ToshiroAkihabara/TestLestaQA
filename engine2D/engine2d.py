import random

class Engine2D:
    
    __INSTANCE = None
    __CANVAS = []
    __COLOR = "Black"
    
    def __new__(cls, *args, **kwargs):
        if cls.__INSTANCE is None:
            cls.__INSTANCE = super().__new__(cls)
        return cls.__INSTANCE
    
    def __del__(cls):
        cls.__INSTANCE = None
        cls.__CANVAS = []
        cls.__COLOR = "Black"

    @classmethod
    def draw(cls):
        return [i.draw() for i in cls.__CANVAS] and cls.__CANVAS.clear()
    
    @classmethod
    def show_canvas(cls):
        print([i.show() for i in cls.__CANVAS])
        return [i.show() for i in cls.__CANVAS]
    
    @classmethod
    def show_color_pencil(cls):
        return cls.__COLOR
    
    @classmethod
    def clear_canvas(cls):
        cls.__CANVAS.clear()

    @classmethod
    def add_circle(cls, radius: int = 5):
        cls.__CANVAS.append(cls.__Circle(cls.__COLOR, radius))

    @classmethod
    def add_triangle(cls, height: int = 2, width: int = 3):
        cls.__CANVAS.append(cls.__Triangle(cls.__COLOR, height, width))

    @classmethod
    def add_rectangle(cls, length: int= 4, width: int = 3):
        cls.__CANVAS.append(cls.__Rectangle(cls.__COLOR, length, width))
          
    @classmethod
    def change_color_pencil(cls):
        colors = ("Orange", "Blue", "Green", "Gold", "Red", "Yellow")
        cls.__COLOR = random.choice(colors)
    
    @classmethod
    def get_circle(cls, color: str, radius: int):
        return cls.__Circle(color=color, radius=radius)
    
    @classmethod
    def get_triangle(cls, color: str, height: int, width: int):
        return cls.__Triangle(color=color, height=height, width=width)
    
    @classmethod
    def get_rectangle(cls, color: str, length: int, width: int):
        return cls.__Rectangle(color=color,length=length, width=width)
    
    class __Circle():
        def __init__(self, color: str, radius: (int, float)) -> None:
            self._name = "Circle"
            if isinstance(radius, (int, float)):
                self._radius = abs(radius)
            else:
                raise TypeError("Use only int and float values")
            self._diameter = 2 * self._radius
            if isinstance(color, str):
                self._color = color
            else:
                raise TypeError("Use only str values")

        def show(self) -> str:
            return self._name
        
        def draw(self) -> str:
            print(f"Drawing Circle with radius {self._radius} and diameter {self._diameter} by {self._color} color")

    class __Triangle():
        def __init__(self, color: str, height: (int, float), width: (int, float)) -> None:
            self._name = "Triangle"
            if isinstance(height, (int, float)) and isinstance(width, (int, float)):
                self._height = abs(height)
                self._width = abs(width)
            else:
                raise TypeError("Use only int and float values")
            if isinstance(color, str):   
                self._color = color 
            else:
                raise TypeError("Use only str values")
            
        def show(self) -> str:
            return self._name
        
        def draw(self) -> str:
            print(f"Drawing Triangle with height {self._height} and wight {self._width} by {self._color} color")

    class __Rectangle():
        def __init__(self, color: str, length: (int, float), width: (int, float)) -> None:
            self._name = "Rectangle"
            if isinstance(length, (int, float)) and isinstance(width, (int, float)):
                self._length = abs(length)
                self._width = abs(width)
            else:
                raise TypeError("Use only int and float values")
            if isinstance(color, str):
                self._color = color
            else:
                raise TypeError("Use only str values")

        def show(self) -> str:
            return self._name
        
        def draw(self) -> str:
            print(f"Drawing Rectangle with length {self._length} and width {self._width} by {self._color} color")

        
