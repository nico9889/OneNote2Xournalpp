from enum import Enum


class Tool(Enum):
    Pen = "pen"
    Eraser = "eraser"
    Highlighter = "highlighter"


class Color(Enum):
    Black = "black"
    Blue = "blue"
    Red = "red"
    Green = "green"
    Gray = "gray"
    LightBlue = "lightblue"
    LightGreen = "lightgreen"
    Magenta = "magenta"
    Orange = "orange"
    Yellow = "yellow"
    White = "white"


class RGBColor:
    def __init__(self, r, g, b) -> None:
        self.r = hex(r).replace("0x", "")
        self.g = hex(g).replace("0x", "")
        self.b = hex(b).replace("0x", "")
        if len(self.r) == 1:
            self.r = "0" + self.r
        if len(self.g) == 1:
            self.g = "0" + self.g
        if len(self.b) == 1:
            self.b = "0" + self.b

    @property
    def value(self) -> str:
        return f"#{self.r}{self.g}{self.b}ff"


class Boundaries:
    def __init__(self, top, left, bottom, right) -> None:
        self.top = top
        self.left = left
        self.bottom = bottom
        self.right = right

    def max(self, other):
        top = max(self.top, other.top)
        left = max(self.left, other.left)
        right = max(self.right, other.right)
        bottom = max(self.bottom, other.bottom)
        return Boundaries(top, left, bottom, right)

    def __repr__(self) -> str:
        return f"Boundaries(t:{self.top}, l:{self.left}, b:{self.bottom}, r:{self.right})"


class Stroke:
    def __init__(self) -> None:
        self._coords = []
        self._color = Color.Black
        self._width = 1
        self._scalex = 1
        self._scaley = 1
        self._tool = Tool.Pen
        self._offsetx = 0
        self._offsety = 0

    def add_point(self, x: int, y: int):
        self._coords.append((x, y))

    def set_width(self, width: float):
        self._width = width

    def set_color(self, color: Color):
        self._color = color

    def set_color_hex(self, r: int, g: int, b: int):
        self._color = RGBColor(r, g, b)

    def set_tool(self, tool: Tool):
        self._tool = tool

    def set_scale_x(self, scale: float):
        self._scalex = scale

    def set_scale_y(self, scale: float):
        self._scaley = scale

    def set_offsets(self, x: int, y: int):
        self._offsetx = x
        self._offsety = y

    def __adjust_x__(self, x):
        return x * self._scalex + self._offsetx

    def __adjust_y__(self, y):
        return y * self._scaley + self._offsety

    def get_boundaries(self) -> Boundaries:
        if len(self._coords) < 0:
            top = 0
            left = 0
            bottom = 0
            right = 0
        else:
            top = self.__adjust_y__(self._coords[0][1])
            left = self.__adjust_x__(self._coords[0][0])
            bottom = self.__adjust_y__(self._coords[0][1])
            right = self.__adjust_x__(self._coords[0][0])
        for x, y in self._coords:
            x = self.__adjust_x__(x)
            y = self.__adjust_y__(y)
            left = left if x > left else x
            right = right if x < right else x
            top = top if y < top else y
            bottom = bottom if y > bottom else y
        return Boundaries(top, left, bottom, right)

    def to_xml(self) -> str:
        if len(self._coords) == 1:
            print("Invalid stroke")
            return ""
        out = f'<stroke tool="{self._tool.value}" color="{self._color.value}" width="{self._width}">\n'
        for x, y in self._coords:
            out += f"{self.__adjust_x__(x)} {self.__adjust_y__(y)} "
        out = out[:-1]
        out += '\n</stroke>'
        # print(out)
        return out
