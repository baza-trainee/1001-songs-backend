from datetime import datetime
from markupsafe import Markup

# class MediaFormatter:
#     def __init__(self, many: bool = False) -> None:
#         self.many = many

#     def __call__(self, m, a):


def format_quill(m, a):
    if field_data := getattr(m, a, None):
        return Markup(f"<div class='quill-column'>{field_data}</div>")


def format_datetime(m, a):
    if field_data := getattr(m, a, None):
        field_data: datetime
        return field_data.strftime("%d/%m/%Y, %H:%M")


def format_array_of_string(m, a):
    if field_data := getattr(m, a, None):
        res = ""
        for data in field_data:
            res += f"<br>{data}"
        return Markup(res)
