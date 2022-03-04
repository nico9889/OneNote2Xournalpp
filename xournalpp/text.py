from .stroke import RGBColor, Boundaries


class Text:
    def __init__(self, text: str = "", font: str = "Sans", size: int = 12, x: int = 0, y: int = 0,
                 color=(0x00, 0x00, 0x00, 0xff), ts: int = 0, fn="", width: int = 0):
        height = size
        if width > 0:
            acc = 0
            self.text = ""
            for c in text:
                acc += size // 2
                if acc > width:
                    acc = 0
                    self.text += "\n"
                    height += size
                self.text += c

        else:
            self.text = text
        self.font = font
        self.size = size
        self.x = x
        self.y = y
        self.color = RGBColor(color[0], color[1], color[2])
        self.ts = ts
        self.fn = fn
        self.width = width
        self.height = height

    def get_boundaries(self) -> Boundaries:
        return Boundaries(self.y, self.x, self.y+self.height, self.x + self.width)


    def to_xml(self) -> str:
        return f"<text font=\"{self.font}\" size=\"{self.size}\" x=\"{self.x}\" y=\"{self.y}\" color=\"{self.color.value}\" ts=\"{self.ts}\" fn=\"{self.fn}\">{self.text}</text>"
