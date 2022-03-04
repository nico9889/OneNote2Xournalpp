from operator import le

from xournalpp.stroke import Boundaries


from .stroke import Boundaries

class Image:
    def __init__(self, data) -> None:
        self.__data__ = data
        self.__left__ = 0
        self.__top__ = 0
        self.__right__ = 0
        self.__bottom__ = 0

    def set_margins(self, left: float, top: float, right: float, bottom: float):
        self.__left__ = left
        self.__top__ = top
        self.__right__ = right
        self.__bottom__ = bottom

    def get_boundaries(self) -> Boundaries:
        return Boundaries(self.__top__, self.__left__, self.__bottom__, self.__right__)

    def to_xml(self):
        return f"<image left=\"{self.__left__}\" top=\"{self.__top__}\" right=\"{self.__right__}\" bottom=\"{self.__bottom__}\">{self.__data__}</image>"
