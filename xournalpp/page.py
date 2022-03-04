from .stroke import Boundaries, Stroke
from .image import Image
from .text import Text

class Background:
    def __init__(self) -> None:
        pass

    def to_xml(self):
        return "<background type=\"solid\" color=\"#ffffffff\" style=\"lined\"/>"


class Layer:
    def __init__(self) -> None:
        self._strokes = []
        self._images = []
        self._texts = []

    def add_text(self, text: Text):
        self._texts.append(text)

    def add_stroke(self, stroke: Stroke):
        self._strokes.append(stroke)

    def add_image(self, image: Image):
        self._images.append(image)

    def get_boundaries(self) -> Boundaries:
        bound = Boundaries(0, 0, 0, 0)
        for stroke in self._strokes:
            bound = bound.max(stroke.get_boundaries())
        print(bound)
        for image in self._images:
            bound = bound.max(image.get_boundaries())
        print(bound)
        for text in self._texts:
            bound = bound.max(text.get_boundaries())
        print(bound)
        return bound

    def to_xml(self):
        out = '<layer>\n'
        for text in self._texts:
            out += text.to_xml() + "\n"
        for stroke in self._strokes:
            out += stroke.to_xml() + "\n"
        for image in self._images:
            out += image.to_xml() + "\n"
        out += "\n</layer>"
        return out


class Page:
    def __init__(self) -> None:
        self._width = 0
        self._height = 0
        self._layers = []
        self._background = Background()

    def add_layer(self, layer: Layer):
        self._layers.append(layer)

    def calculate(self):
        bound = Boundaries(0, 0, 0, 0)
        for layer in self._layers:
            bound = bound.max(layer.get_boundaries())
        self._width = bound.right
        self._height = bound.top + 10

    def to_xml(self):
        out = f"<page width=\"{self._width}\" height=\"{self._height}\">\n"
        out += "<layer>\n"
        out += self._background.to_xml() + "\n"
        out += "</layer>\n"
        for layer in self._layers:
            out += layer.to_xml() + "\n"
        out += "\n</page>"
        return out
