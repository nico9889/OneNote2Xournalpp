import gzip
from .page import Page

class Document:
    def __init__(self, title) -> None:
        self.title = title
        self.__pages__ = []

    def add_page(self, page: Page):
        self.__pages__.append(page)

    def to_xml(self):
        for page in self.__pages__:
            page.calculate()
        out = "<?xml version=\"1.0\" standalone=\"no\"?>\n"
        out += "<xournal creator=\"OneNote Converter Script\" fileversion=\"4\">\n"
        out += f"<title>{self.title}</title>\n"
        out += "<preview></preview>\n"
        for page in self.__pages__:
            out += page.to_xml() + "\n"
        out+="</xournal>"
        return out

    def export(self):
        data = self.to_xml()
        with gzip.open(f"{self.title}.xopp", "wb") as f:
            f.write(data.encode("UTF-8"))
