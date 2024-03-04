from datetime import datetime
from typing import Literal
from markupsafe import Markup

from src.config import settings


class MediaFormatter:
    def __init__(
        self,
        file_type: Literal["photo", "document", "audio"] = "photo",
        heigth: int = 120,
    ) -> None:
        self.file_type = file_type
        self.heigth = heigth

    def __call__(self, m, a):
        grid_html = ""
        if media := getattr(m, a, None):
            match self.file_type:
                case "photo":
                    grid_html = f'<img style="height: {self.heigth}px;" class="grid-image" src="{settings.BASE_URL}/{media}">'
                case "document":
                    icon_url = f"{settings.BASE_URL}/static/interface/pdf_icon.svg"
                    grid_html = f'<a href="{settings.BASE_URL}/{media}" target="_blank"><img class="grid-pdf" src="{icon_url}"></a>'
                case "audio":
                    grid_html += (
                        f'<audio controls class="grid-audio">'
                        f'<source src="{settings.BASE_URL}/{media}" type="audio/mp3">'
                        f"Your browser does not support the audio element.</audio>"
                    )
        return Markup(grid_html)


class PhotoSplitFormatter:
    def __init__(self, media_fields: list[str]) -> None:
        self.media_fields = media_fields

    def __call__(self, m, a):
        grid_html = '<div class="grid-split-image-container">'
        for field in self.media_fields:
            image = getattr(m, field, None)
            if image:
                grid_html += (
                    f'<img class="grid-split-image" src={settings.BASE_URL}/{image}>'
                )
        grid_html += "<div>"
        return Markup(grid_html)


class TextFormatter:
    def __init__(
        self,
        text_align: Literal["left", "center"] = "center",
        min_width: int = 150,
        max_lenth: int = None,
        to_bool: bool = None,
    ) -> None:
        "min_width: **px"
        self.text_align = text_align
        self.min_width = min_width
        self.max_lenth = max_lenth
        self.to_bool = to_bool

    def __call__(self, m, a):
        text = getattr(m, a, None)
        grid_html = ""
        self.max_width = "auto"
        if self.max_lenth:
            text = text[: self.max_lenth] + (
                "..." if len(text) >= self.max_lenth else ""
            )
        if self.to_bool:
            text = '<b style="font-size: 20px">' + ("+" if text else "-") + "</b>"
            self.min_width = 1
            self.max_width = 10
        if text:
            grid_html = f'<div style="text-align: {self.text_align}; min-width: {self.min_width}px; max_width={self.max_width}px">{text}</div>'
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


class ArrayFormatter:
    def __init__(self, width: int = "auto") -> None:
        self.width = width

    def __call__(self, m, a):
        res = ""
        if field_data := getattr(m, a, None):
            for data in field_data:
                res += f'<div style="width:{self.width*2}px;"><p class="grid-string-array", style="width:{self.width}px;">{data}</p></div>'
        return Markup(res)
