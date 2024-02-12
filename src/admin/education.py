# import asyncio
# from typing import Any
# from uuid import uuid4
# from fastapi import Request
# from markupsafe import Markup
# from sqladmin import ModelView
# from wtforms import TextAreaField

# from src.config import settings
# from src.education.models import EducationSection
# from src.utils import MediaValidator, delete_photo

# MEDIA_FIELDS = [
#     "media1",
#     "media2",
#     "media3",
#     "media4",
#     "media5",
# ]


# class EducationAdmin(ModelView, model=EducationSection):
#     name_plural = "Освітний розділ"
#     icon = "fa-solid fa-user-graduate"

#     column_list = [
#         EducationSection.title,
#         EducationSection.description,
#         EducationSection.media1,
#     ]

#     def _image_formatter(m, a):
#         grid_html = ""
#         for field in MEDIA_FIELDS:
#             image = getattr(m, field, None)
#             if image:
#                 grid_html += f'<img class="grid-item" src={settings.BASE_URL}/{image}>'
#         return Markup(grid_html)

#     column_formatters = {EducationSection.media1: _image_formatter}
#     column_details_exclude_list = ["id"]

#     can_edit = True
#     can_create = True
#     can_delete = True

#     form_overrides = {
#         "description": TextAreaField,
#     }
#     form_args = {
#         **{field: {"validators": [MediaValidator()]} for field in MEDIA_FIELDS},
#         "description": {
#             "render_kw": {
#                 "class": "form-control",
#                 "rows": 7,
#             },
#         },
#     }

#     async def on_model_change(
#         self, data: dict, model: Any, is_created: bool, request: Request
#     ) -> None:
#         field_to_del = []
#         for field, field_data in data.items():
#             if field in MEDIA_FIELDS:
#                 if field_data.size:
#                     file_name = f'{uuid4().hex}.{field_data.filename.split(".")[-1]}'
#                     if is_created:
#                         data[field].filename = file_name
#                     else:
#                         model_data = getattr(model, field, None)
#                         if model_data and model_data != field_data.filename:
#                             data[field].filename = file_name
#                             await delete_photo(model_data)
#                 else:
#                     field_to_del.append(field)
#         for field in field_to_del:
#             del data[field]
#         return await super().on_model_change(data, model, is_created, request)

#     async def on_model_delete(self, model: Any, request: Request) -> None:
#         for field in MEDIA_FIELDS:
#             field_data = getattr(model, field, None)
#             await delete_photo(field_data)
#         return await super().on_model_delete(model, request)
