from typing import Union


class TextMixin:

    ### CLASS VARIABLES ###

    __documentation_section__ = 'HTML Mixin Classes'

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        bold: bool=None,
        font_color: str=None,
        font_face: str=None,
        font_size: Union[int, float]=None,
        italic: bool=None,
        overlined: bool=None,
        strikethrough: bool=None,
        underlined: bool=None,
        ) -> None:
        self.bold = bold
        self.font_color = font_color
        self.font_face = font_face
        self.font_size = font_size
        self.italic = italic
        self.overlined = overlined
        self.strikethrough = strikethrough
        self.underlined = underlined

    ### PUBLIC PROPERTIES ###

    @property
    def bold(self):
        return self._bold

    @bold.setter
    def bold(self, bold):
        if bold is not None:
            bold = bool(bold)
        self._bold = bold

    @property
    def font_color(self):
        return self._font_color

    @font_color.setter
    def font_color(self, font_color):
        if font_color is not None:
            font_color = str(font_color)
        self._font_color = font_color

    @property
    def font_face(self):
        return self._font_face

    @font_face.setter
    def font_face(self, font_face):
        if font_face is not None:
            font_face = str(font_face)
        self._font_face = font_face

    @property
    def font_size(self):
        return self._font_size

    @font_size.setter
    def font_size(self, font_size):
        if font_size is not None:
            font_size = float(font_size)
        self._font_size = font_size

    @property
    def italic(self):
        return self._italic

    @italic.setter
    def italic(self, italic):
        if italic is not None:
            italic = bool(italic)
        self._italic = italic

    @property
    def overlined(self):
        return self._overlined

    @overlined.setter
    def overlined(self, overlined):
        if overlined is not None:
            overlined = bool(overlined)
        self._overlined = overlined

    @property
    def strikethrough(self):
        return self._strikethrough

    @strikethrough.setter
    def strikethrough(self, strikethrough):
        if strikethrough is not None:
            strikethrough = bool(strikethrough)
        self._strikethrough = strikethrough

    @property
    def underlined(self):
        return self._underlined

    @underlined.setter
    def underlined(self, underlined):
        if underlined is not None:
            underlined = bool(underlined)
        self._underlined = underlined
