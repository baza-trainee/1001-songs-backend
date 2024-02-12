import asyncio
from typing import Any
from uuid import uuid4
from fastapi import Request
from markupsafe import Markup
from sqladmin import ModelView
from wtforms import TextAreaField
from src.admin.commons.validators import MediaValidator

from src.config import settings
from src.education.models import (
    EducationPage,
    CalendarAndRitualCategory,
    SongSubcategory,
    EducationPageSongGenre,
)
from src.utils import delete_photo


MEDIA_FIELDS = [
    "media1",
    "media2",
    "media3",
    "media4",
    "media5",
]


class EducationAdmin(ModelView, model=EducationPage):
    is_async = True
    can_edit = True
    can_create = False
    can_delete = False
    can_export = False

    category = "Освітний розділ"
    name_plural = "Загальна інформація"
    icon = "fa-solid fa-user-graduate"

    column_list = [
        EducationPage.title,
        EducationPage.description,
        EducationPage.recommendations,
        EducationPage.recommended_sources,
    ]
    column_labels = {
        EducationPage.title: "Заголовок розділу",
        EducationPage.description: "Опис",
        EducationPage.recommendations: "Рекомендації",
        EducationPage.recommended_sources: "Рекомендовані джерела",
    }
    column_details_exclude_list = ["id"]

    form_overrides = {
        "description": TextAreaField,
        "recommendations": TextAreaField,
        "recommended_sources": TextAreaField,
    }
    form_args = {
        "description": {
            "render_kw": {
                "class": "form-control",
                "rows": 7,
            },
        },
        "recommendations": {
            "render_kw": {
                "class": "form-control",
                "rows": 7,
            },
        },
        "recommended_sources": {
            "render_kw": {
                "class": "form-control",
                "rows": 7,
            },
        },
    }


class CalendarAndRitualCategoryAdmin(ModelView, model=CalendarAndRitualCategory):
    is_async = True
    name_plural = "Пісенні розділи"
    category = "Освітний розділ"
    can_create = False
    can_delete = False
    can_export = False
    column_list = [
        CalendarAndRitualCategory.title,
        CalendarAndRitualCategory.media,
        CalendarAndRitualCategory.description,
        CalendarAndRitualCategory.recommended_sources,
    ]
    column_labels = {
        CalendarAndRitualCategory.title: "Назва розділу",
        CalendarAndRitualCategory.media: "Фото",
        CalendarAndRitualCategory.description: "Опис",
        CalendarAndRitualCategory.recommended_sources: "Рекомендовані джерела",
        CalendarAndRitualCategory.education_genres: "Жанри категорій",
        CalendarAndRitualCategory.song_subcategories: "Підкатегорії",
    }
    form_columns = [
        CalendarAndRitualCategory.title,
        CalendarAndRitualCategory.media,
        CalendarAndRitualCategory.description,
        CalendarAndRitualCategory.recommended_sources,
    ]
    form_overrides = {
        "description": TextAreaField,
        "recommended_sources": TextAreaField,
    }
    form_args = {
        "description": {
            "render_kw": {
                "class": "form-control",
                "rows": 7,
            },
        },
        "recommended_sources": {
            "render_kw": {
                "class": "form-control",
                "rows": 7,
            },
        },
        "media": {"validators": [MediaValidator()]},
    }

    async def on_model_change(
        self, data: dict, model: Any, is_created: bool, request: Request
    ) -> None:
        field_to_del = []
        for field, field_data in data.items():
            if field == "media":
                if field_data.size:
                    file_name = f'{uuid4().hex}.{field_data.filename.split(".")[-1]}'
                    if is_created:
                        data[field].filename = file_name
                    else:
                        model_data = getattr(model, field, None)
                        if model_data and model_data != field_data.filename:
                            data[field].filename = file_name
                            await delete_photo(model_data)
                else:
                    field_to_del.append(field)
        for field in field_to_del:
            del data[field]
        return await super().on_model_change(data, model, is_created, request)

    async def on_model_delete(self, model: Any, request: Request) -> None:
        field_data = getattr(model, "media", None)
        await delete_photo(field_data)
        return await super().on_model_delete(model, request)

    def _image_formatter(m, a):
        grid_html = ""
        image = getattr(m, "media", None)
        if image:
            grid_html += f'<img class="grid-item" src={settings.BASE_URL}/{image}>'
        return Markup(grid_html)

    column_formatters = {CalendarAndRitualCategory.media: _image_formatter}


class SongSubcategoryAdmin(ModelView, model=SongSubcategory):
    is_async = True
    name_plural = "Пісенні категорії"
    category = "Освітний розділ"
    can_create = True
    can_delete = True
    can_export = False
    column_list = [
        SongSubcategory.media,
        SongSubcategory.title,
        SongSubcategory.main_category,
    ]
    column_labels = {
        SongSubcategory.title: "Назва категорії",
        SongSubcategory.media: "Фото",
        SongSubcategory.main_category: "Розділ",
        SongSubcategory.education_genres: "Жанри",
    }
    form_columns = [
        SongSubcategory.title,
        SongSubcategory.media,
        SongSubcategory.main_category,
    ]
    column_details_list = [
        SongSubcategory.title,
        SongSubcategory.media,
        SongSubcategory.main_category,
        SongSubcategory.education_genres,
    ]


class EducationPageSongGenreAdmin(ModelView, model=EducationPageSongGenre):
    is_async = True
    name_plural = "Пісенні жанри"
    category = "Освітний розділ"
    can_create = True
    can_delete = True
    can_export = False
    column_list = form_columns = column_details_list = [
        EducationPageSongGenre.title,
        EducationPageSongGenre.description,
        EducationPageSongGenre.sub_category,
        EducationPageSongGenre.media1,
        EducationPageSongGenre.media2,
        EducationPageSongGenre.media3,
        EducationPageSongGenre.media4,
        EducationPageSongGenre.media5,
    ]
    column_labels = {
        EducationPageSongGenre.title: "Назва жанру",
        EducationPageSongGenre.sub_category: "Категорія",
        EducationPageSongGenre.description: "Опис",
        EducationPageSongGenre.media1: "Фото",
        EducationPageSongGenre.media2: "Фото",
        EducationPageSongGenre.media3: "Фото",
        EducationPageSongGenre.media4: "Фото",
        EducationPageSongGenre.media5: "Фото",
    }
    form_overrides = {
        "description": TextAreaField,
    }
    form_args = {
        "description": {
            "render_kw": {
                "class": "form-control",
                "rows": 7,
            },
        },
        **{field: {"validators": [MediaValidator()]} for field in MEDIA_FIELDS},
    }

    # def _image_formatter(m, a):
    #     grid_html = ""
    #     for field in MEDIA_FIELDS:
    #         image = getattr(m, field, None)
    #         if image:
    #             grid_html += f'<img class="grid-item" src={settings.BASE_URL}/{image}>'
    #     return Markup(grid_html)

    # column_formatters = {
    #     EducationPageSongGenre.media1: _image_formatter,
    #     EducationPageSongGenre.media2: _image_formatter,
    #     EducationPageSongGenre.media3: _image_formatter,
    #     EducationPageSongGenre.media4: _image_formatter,
    #     EducationPageSongGenre.media5: _image_formatter,
    # }

    async def on_model_change(
        self, data: dict, model: Any, is_created: bool, request: Request
    ) -> None:
        field_to_del = []
        for field, field_data in data.items():
            if field in MEDIA_FIELDS:
                if field_data.size:
                    file_name = f'{uuid4().hex}.{field_data.filename.split(".")[-1]}'
                    if is_created:
                        data[field].filename = file_name
                    else:
                        model_data = getattr(model, field, None)
                        if model_data and model_data != field_data.filename:
                            data[field].filename = file_name
                            await delete_photo(model_data)
                else:
                    field_to_del.append(field)
        for field in field_to_del:
            del data[field]
        return await super().on_model_change(data, model, is_created, request)

    async def on_model_delete(self, model: Any, request: Request) -> None:
        for field in MEDIA_FIELDS:
            field_data = getattr(model, field, None)
            await delete_photo(field_data)
        return await super().on_model_delete(model, request)
