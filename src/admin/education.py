from typing import Any

from fastapi import Form, Request
from sqladmin import ModelView
from wtforms import TextAreaField

from src.admin.commons.formatters import (
    MediaFormatter,
    MediaSplitFormatter,
    format_array_of_string,
    format_quill,
)
from src.admin.commons.utils import model_change_for_editor, model_change_for_files
from src.admin.commons.validators import MediaValidator
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
    column_details_exclude_list = [
        EducationPage.id,
    ]

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
    }
    column_formatters = {
        EducationPage.recommendations: format_array_of_string,
        EducationPage.recommended_sources: format_quill,
    }
    column_formatters = {
        EducationPage.recommendations: format_quill,
        EducationPage.recommended_sources: format_array_of_string,
    }

    async def scaffold_form(self) -> type[Form]:
        form = await super().scaffold_form()
        form.is_editor_field = [
            "recommendations",
        ]
        del form.recommendations.kwargs["validators"][-1]
        return form

    async def on_model_change(
        self, data: dict, model: Any, is_created: bool, request: Request
    ) -> None:
        await model_change_for_editor(data, model, field_name="recommendations")
        return await super().on_model_change(data, model, is_created, request)


class CalendarAndRitualCategoryAdmin(ModelView, model=CalendarAndRitualCategory):
    is_async = True

    name_plural = "Освітні категорії"
    category = "Освітний розділ"
    icon = "fa-solid fa-layer-group"

    can_create = False
    can_delete = False
    can_export = False
    column_list = [
        CalendarAndRitualCategory.title,
        CalendarAndRitualCategory.media,
        CalendarAndRitualCategory.description,
        CalendarAndRitualCategory.recommended_sources,
    ]
    column_details_list = [
        CalendarAndRitualCategory.title,
        CalendarAndRitualCategory.media,
        CalendarAndRitualCategory.description,
        CalendarAndRitualCategory.recommended_sources,
        CalendarAndRitualCategory.education_genres,
        CalendarAndRitualCategory.song_subcategories,
    ]
    column_labels = {
        CalendarAndRitualCategory.title: "Назва категорії",
        CalendarAndRitualCategory.media: "Фото",
        CalendarAndRitualCategory.description: "Опис",
        CalendarAndRitualCategory.recommended_sources: "Рекомендовані джерела",
        CalendarAndRitualCategory.education_genres: "Жанри",
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
    }
    column_formatters = {
        CalendarAndRitualCategory.recommended_sources: format_array_of_string,
        CalendarAndRitualCategory.media: MediaFormatter(),
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

        return await super().on_model_change(data, model, is_created, request)

    async def on_model_delete(self, model: Any, request: Request) -> None:
        field_data = getattr(model, "media", None)
        await delete_photo(field_data)
        return await super().on_model_delete(model, request)


class SongSubcategoryAdmin(ModelView, model=SongSubcategory):
    is_async = True

    name_plural = "Освітні під-категорії"
    category = "Освітний розділ"
    icon = "fa-solid fa-layer-group"

    can_create = True
    can_delete = True
    can_export = False

    column_list = [
        SongSubcategory.media,
        SongSubcategory.title,
        SongSubcategory.main_category,
    ]
    column_labels = {
        SongSubcategory.title: "Назва під-категорії",
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
    column_formatters = {
        SongSubcategory.media: MediaFormatter(),
    }

    async def on_model_change(
        self, data: dict, model: Any, is_created: bool, request: Request
    ) -> None:
        fields = ["media"]
        await model_change_for_files(data, model, is_created, fields)
        return await super().on_model_change(data, model, is_created, request)

    async def on_model_delete(self, model: Any, request: Request) -> None:
        await delete_photo(getattr(model, "media", None))
        return await super().on_model_delete(model, request)


class EducationPageSongGenreAdmin(ModelView, model=EducationPageSongGenre):
    is_async = True

    name_plural = "Освітні жанри"
    category = "Освітний розділ"
    icon = "fa-solid fa-layer-group"

    can_create = True
    can_delete = True
    can_export = False

    column_list = form_columns = column_details_list = [
        EducationPageSongGenre.title,
        EducationPageSongGenre.description,
        EducationPageSongGenre.sub_category,
        EducationPageSongGenre.media1,
    ]
    column_labels = {
        EducationPageSongGenre.title: "Назва жанру",
        EducationPageSongGenre.sub_category: "Категорія",
        EducationPageSongGenre.description: "Опис",
        EducationPageSongGenre.media1: "Фото",
        EducationPageSongGenre.media2: "Фото 2",
        EducationPageSongGenre.media3: "Фото 3",
        EducationPageSongGenre.media4: "Фото 4",
        EducationPageSongGenre.media5: "Фото 5",
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
    column_formatters = {
        EducationPageSongGenre.media1: MediaSplitFormatter(MEDIA_FIELDS),
    }

    async def on_model_change(
        self, data: dict, model: Any, is_created: bool, request: Request
    ) -> None:
        await model_change_for_files(data, model, is_created, MEDIA_FIELDS)
        return await super().on_model_change(data, model, is_created, request)

    async def on_model_delete(self, model: Any, request: Request) -> None:
        for field in MEDIA_FIELDS:
            field_data = getattr(model, field, None)
            await delete_photo(field_data)
        return await super().on_model_delete(model, request)
