from datetime import datetime
from typing import Literal
from markupsafe import Markup

from src.config import settings


class MediaFormatter:
    def __init__(self, is_file: bool = False, is_audio: bool = False) -> None:
        self.is_file = is_file
        self.is_audio = is_audio

    def __call__(self, m, a):
        grid_html = ""
        if media := getattr(m, a, None):
            if self.is_audio:
                grid_html += (
                    f'<audio controls class="grid-audio">'
                    f'<source src="{settings.BASE_URL}/{media}" type="audio/mp3">'
                    f"Your browser does not support the audio element.</audio>"
                )
            elif self.is_file:
                icon_url = f"{settings.BASE_URL}/static/interface/pdf_icon.svg"
                grid_html = f'<a href="{settings.BASE_URL}/{media}" target="_blank"><img class="grid-pdf" src="{icon_url}"></a>'
            else:
                grid_html = (
                    f'<img class="grid-image" src="{settings.BASE_URL}/{media}">'
                )
        return Markup(grid_html)


class MediaSplitFormatter:
    def __init__(self, media_fields: list[str]) -> None:
        self.media_fields = media_fields

    def __call__(self, m, a):
        grid_html = ""
        for field in self.media_fields:
            image = getattr(m, field, None)
            if image:
                grid_html += (
                    f'<img class="grid-split-image" src={settings.BASE_URL}/{image}>'
                )
        return Markup(grid_html)


class TextFormatter:
    def __init__(
        self, text_align: Literal["left", "center"] = "center", min_width: int = 150
    ) -> None:
        "min_width: **px"
        self.text_align = text_align
        self.min_width = min_width

    def __call__(self, m, a):
        text = getattr(m, a, None)
        grid_html = ""
        if text:
            grid_html = f'<div style="text-align: {self.text_align}; min-width: {self.min_width}px;">{text}</div>'
        return Markup(grid_html)


def format_quill(m, a):
    if field_data := getattr(m, a, None):
        return Markup(f'<div class="quill-column">{field_data}</div>')


def format_datetime(m, a):
    if field_data := getattr(m, a, None):
        field_data: datetime
        return field_data.strftime("%d/%m/%Y, %H:%M")


def format_date(m, a):
    res = ""
    if field_data := getattr(m, a, None):
        res = field_data.strftime("%d/%m/%Y")
    return res


def format_array_of_string(m, a):
    res = ""
    if field_data := getattr(m, a, None):
        for data in field_data:
            res += f'<p class="grid-string-array">{data}</p>'
    return Markup(res)
