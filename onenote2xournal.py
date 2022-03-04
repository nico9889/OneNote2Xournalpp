import re
from bs4 import BeautifulSoup
import sys
from xournalpp.document import Document
from xournalpp.image import Image
from xournalpp.page import Layer, Page
from xournalpp.stroke import Stroke
from xournalpp.text import Text

from xml.sax.saxutils import escape

if len(sys.argv) < 3:
    print("python3 ./onenote2xournal.py input_file.html output_file_name")
    exit(1)

# DO NOT CHANGE, I DON'T KNOW WHY THIS IS THE ONLY SCALE THAT WORKS
SCALE_X = 0.04
SCALE_Y = 0.04

print(sys.argv[1])

page = None

with open(sys.argv[1], "r") as f:
    page = f.read()

if not page:
    print("Coudln't import page")
    sys.exit(1)


# Utility class to store SVG strokes
class Line:
    def __init__(self, offsetx: int, offsety: int, width: float) -> None:
        self.coords = []
        self.offsetx = offsetx
        self.offsety = offsety
        self.color = None
        self.scalex = SCALE_X
        self.scaley = SCALE_Y
        self.width = width

    def addCoord(self, x: int, y: int):
        self.coords.append((x, y))

    def setColorHex(self, r: int, g: int, b: int):
        self.color = (r, g, b)


# Function to extract SVG strokes. Apparently a single stroke can be composed by
# separated line, we need to extract them all to convert them into Xournal compatible strokes
def get_lines(path):
    out = []
    svg = path.parent
    stroke_width = float(path["stroke-width"]) / 25
    left = re.search("(^|\s)left: (\d+)px", svg["style"])
    left = 0 if not left else int(left.groups()[1])

    top = re.search("(^|\s)top: (\d+)px", svg["style"])
    top = 0 if not top else int(top.groups()[1])

    width = re.search("(^|\s)width: (\d+)px", svg["style"])
    width = 1 if not width else int(width.groups()[1])

    height = re.search("(^|\s)height: (\d+)px", svg["style"])
    height = 1 if not height else int(height.groups()[1])

    viewbox = re.search("(\d+) (\d+) (\d+) (\d+)", svg["viewbox"])
    viewx = int(viewbox.groups()[0]) if viewbox else 0
    viewy = int(viewbox.groups()[1]) if viewbox else 0
    vieww = int(viewbox.groups()[2]) if viewbox else 1
    viewh = int(viewbox.groups()[3]) if viewbox else 1

    d = path["d"]
    stroke = path["stroke"]
    color = None
    if stroke:
        rgb = re.search("rgb\((\d+),(\d+),(\d+)\)", stroke)
        if rgb:
            r = int(rgb.groups()[0])
            g = int(rgb.groups()[1])
            b = int(rgb.groups()[2])
            color = (r, g, b)
    moves = re.findall("M (\d+ \d+)", d)
    lines = re.findall("l ([-?\d+ ]+)", d)
    if len(moves) != len(lines):
        print("Not managed case: moves length is different by lines length")
    else:
        for i in range(len(lines)):
            move = moves[i]
            line = lines[i]
            movex, movey = move.split(" ")
            l = Line(left, top, stroke_width)
            l.addCoord(int(movex) - viewx, int(movey) - viewy)
            if color:
                l.setColorHex(color[0], color[1], color[2])
            coords = line.strip().split(" ")
            for j in range(0, len(coords), 2):
                l.addCoord(int(coords[j]), int(coords[j + 1]))
            out.append(l)
    return out


# Function to convert a Line into a Stroke compatible with Xournal
def convert_stroke(line: Line) -> Stroke:
    stroke = Stroke()
    stroke.set_width(line.width)
    stroke.set_offsets(line.offsetx, line.offsety)
    stroke.set_scale_x(line.scalex)
    stroke.set_scale_y(line.scaley)
    if line.color:
        stroke.set_color_hex(line.color[0], line.color[1], line.color[2])

    xs = []
    ys = []

    accx = 0
    accy = 0

    for coord in line.coords:
        accx += coord[0]
        accy += coord[1]
        xs.append(accx)
        ys.append(accy)

    for i in range(len(xs)):
        stroke.add_point(xs[i], ys[i])
    return stroke


# Parsing the HTML page
soup = BeautifulSoup(page, "html.parser")

# Getting all the strokes
paths = soup.find_all("path", class_="RegularInkStroke")

# Generating a page layer
layer = Layer()

for path in paths:
    lines = get_lines(path)
    for line in lines:
        stroke = convert_stroke(line)
        layer.add_stroke(stroke)

# Getting all the images
image_containers = soup.find_all("div", class_="WACImageContainer")
outline_containers = soup.find_all("div", class_="OutlineContainer OutlineContainerDisplayWrapper Ltr")


# FIXME: this is an awful way to realign all the texts
title = soup.find("div", class_="Title GrowUnderline")


title_left = re.search("(^|\s)left: (\d+)px", title["style"])
title_left = 0 if not title_left else int(title_left.groups()[1])

title_top = re.search("(^|\s)top: (\d+)px", title["style"])
title_top = 0 if not title_top else int(title_top.groups()[1])

title_padding_left = re.search("(^|\s)padding-left: (\d+)px", title["style"])
title_padding_left = 0 if not title_padding_left else int(title_padding_left.groups()[1])

title_padding_top = re.search("(^|\s)padding-top: (\d+)px", title["style"])
title_padding_top = 0 if not title_padding_top else int(title_padding_top.groups()[1])

page_offset_x = title_left + title_padding_left
page_offset_y = title_top + title_padding_top  # FIXME: remove, find a proper value dynamically
base_offset_x = 0
base_offset_y = 0
for container in outline_containers:
    base_x = re.search("(^|\s)left: (\d+)px", container["style"])
    base_x = int(base_x.groups()[1]) if base_x else 0
    base_offset_x += base_x

    base_y = re.search("(^|\s)top: (\d+)px", container["style"])
    base_y = int(base_y.groups()[1]) if base_x else 0
    base_offset_y += base_y

    outline = container.find("div", class_="Outline")
    width = 0

    if outline:
        width = re.search("(^|\s)min-width: (\d+)px", outline["style"])
        width = 0 if not width else int(width.groups()[1])

        pad_x = re.search("(^|\s)padding-left: (\d+)px", container["style"])
        pad_x = int(pad_x.groups()[1]) if pad_x else 0

        pad_y = re.search("(^|\s)padding-top: (\d+)px", container["style"])
        pad_y = int(pad_y.groups()[1]) if pad_x else 0

        base_x += pad_x
        base_y += pad_y

    texts = container.find_all("span", class_="TextRun")
    offset = 0
    for text in texts:
        # FIXME: missing text wrap
        size = re.search("(^|\s)font-size: (\d+)pt", text["style"])
        if size:
            size = int(size.groups()[1])
            t = text.find("span", class_="NormalTextRun")
            if t:
                x = base_x + page_offset_x if base_x > 0 else base_offset_x + page_offset_x
                y = (base_y + offset + page_offset_y) if base_y > 0 else (base_offset_y + offset + page_offset_y)
                layer.add_text(Text(escape(t.text), size=size, width=width, x=x, y=y))
                offset += size
                base_offset_y += size

# Converting all the images to a Xournal compatible format (Hurray! They both use images encoded in base64!)
for container in image_containers:
    top = re.search("(^|\s)top: (\d+)px", container["style"])
    if not top:
        outline_container = container.find_previous("div", class_="OutlineContainer OutlineContainerDisplayWrapper Ltr")
        if not outline_container:
            top = 0
        else:
            top = re.search("(^|\s)top: (\d+)px", outline_container["style"])
            top = 0 if not top else float(top.groups()[1])
    else:
        top = float(top.groups()[1])

    left = re.search("(^|\s)left: (\d+)px", container["style"])
    if not left:
        outline_container = container.find_previous("div", class_="OutlineContainer OutlineContainerDisplayWrapper Ltr")
        if not outline_container:
            left = 0
        else:
            left = re.search("(^|\s)left: (\d+)px", outline_container["style"])
            left = 0 if not left else float(left.groups()[1])
    else:
        left = float(left.groups()[1])
    image = container.find("img")
    width = re.search("width: (\d+)px", image["style"])
    if width:
        width = float(width.groups()[0])
    height = re.search("height: (\d+)px", image["style"])
    if height:
        height = float(height.groups()[0])
    img = Image(image["src"].replace("data:image/png;base64,", ""))
    img.set_margins(left, top, width + left, height + top)
    layer.add_image(img)

# Creating the document
doc = Document(sys.argv[2])

# Adding a page
page = Page()
page.add_layer(layer)
doc.add_page(page)

# Exporting the document
doc.export()
