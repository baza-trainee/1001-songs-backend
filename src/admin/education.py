from typing import Any
from fastapi import Request
from wtforms import TextAreaField
from wtforms.validators import DataRequired

from src.admin.commons.base import BaseAdmin
from src.admin.commons.exceptions import IMG_REQ
from src.admin.commons.formatters import (
    MediaFormatter,
    PhotoSplitFormatter,
    TextFormatter,
    format_quill,
)
from src.admin.commons.utils import MediaInputWidget
from src.admin.commons.validators import MediaValidator, QuillValidator
from src.config import IMAGE_TYPES, MAX_IMAGE_SIZE_MB
from src.database.redis import invalidate_cache
from src.education.models import (
    EducationPage,
    CalendarAndRitualCategory,
    SongSubcategory,
    EducationPageSongGenre,
)

RECOMMENDATIONS_PHOTO_RES = (1780, 1090)
CATEGORY_MEDIA_RES = (820, 560)
EDUCATION_PAGE_PHOTO_FIELDS = [
    "media1",
    "media2",
    "media3",
    "media4",
    "media5",
]


class EducationAdmin(BaseAdmin, model=EducationPage):
    category = "Освітний розділ"
    name_plural = "Сторінка розділу"
    icon = "fa-solid fa-user-graduate"

    can_create = False
    can_delete = False

    column_labels = {
        EducationPage.title: "Заголовок",
        EducationPage.description: "Опис",
        EducationPage.recommendations: "Рекомендації",
        EducationPage.recommended_sources: "Рекомендовані джерела",
    }
    column_list = form_columns = [
        EducationPage.title,
        EducationPage.description,
        EducationPage.recommendations,
        EducationPage.recommended_sources,
    ]
    column_formatters = {
        EducationPage.description: TextFormatter(text_align="left", min_width=300),
        EducationPage.recommendations: format_quill,
        EducationPage.recommended_sources: format_quill,
    }
    form_overrides = {
        "description": TextAreaField,
    }
    form_args = {
        "description": {
            "render_kw": {
                "class": "form-control",
                "rows": 7,
                "maxlength": EducationPage.description.type.length,
            },
        },
        "recommendations": {
            "description": IMG_REQ % RECOMMENDATIONS_PHOTO_RES,
        },
        "recommended_sources": {"validators": [QuillValidator(max_text_len=600)]},
    }
    form_quill_list = [
        EducationPage.recommendations,
        EducationPage.recommended_sources,
    ]

    async def after_model_change(
        self, data: dict, model: Any, is_created: bool, request: Request
    ) -> None:
        await invalidate_cache("get_education_page")
        return await super().after_model_change(data, model, is_created, request)


class CalendarAndRitualCategoryAdmin(BaseAdmin, model=CalendarAndRitualCategory):
    name_plural = "Освітні категорії"
    category = "Освітний розділ"
    icon = "fa-solid fa-layer-group"

    can_create = False
    can_delete = False

    column_list = column_details_list = [
        CalendarAndRitualCategory.title,
        CalendarAndRitualCategory.media,
        CalendarAndRitualCategory.description,
        CalendarAndRitualCategory.recommended_sources,
        CalendarAndRitualCategory.education_genres,
        CalendarAndRitualCategory.song_subcategories,
    ]
    form_columns = [
        CalendarAndRitualCategory.title,
        CalendarAndRitualCategory.media,
        CalendarAndRitualCategory.description,
        CalendarAndRitualCategory.recommended_sources,
    ]
    column_labels = {
        CalendarAndRitualCategory.title: "Назва категорії",
        CalendarAndRitualCategory.media: "Фото",
        CalendarAndRitualCategory.description: "Опис",
        CalendarAndRitualCategory.recommended_sources: "Рекомендовані джерела",
        CalendarAndRitualCategory.education_genres: "Жанри",
        CalendarAndRitualCategory.song_subcategories: "Підкатегорії",
    }
    column_searchable_list = [
        CalendarAndRitualCategory.title,
    ]
    column_formatters = {
        CalendarAndRitualCategory.recommended_sources: format_quill,
        CalendarAndRitualCategory.media: MediaFormatter(),
        CalendarAndRitualCategory.description: format_quill,
    }
    form_quill_list = [
        CalendarAndRitualCategory.recommended_sources,
    ]
    form_files_list = [
        CalendarAndRitualCategory.media,
    ]
    form_overrides = {
        "description": TextAreaField,
    }
    form_args = {
        "recommended_sources": {"validators": [QuillValidator(max_text_len=600)]},
        "description": {
            "render_kw": {
                "class": "form-control",
                "rows": 7,
                "maxlength": CalendarAndRitualCategory.description.type.length,
            },
        },
        "media": {
            "widget": MediaInputWidget(is_required=True),
            "validators": [
                MediaValidator(
                    media_types=IMAGE_TYPES,
                    max_size=MAX_IMAGE_SIZE_MB,
                    is_required=True,
                )
            ],
            "description": IMG_REQ % CATEGORY_MEDIA_RES,
        },
    }

    async def after_model_change(
        self, data: dict, model: Any, is_created: bool, request: Request
    ) -> None:
        await invalidate_cache("get_education_page")
        await invalidate_cache("get_category", model.id)
        return await super().after_model_change(data, model, is_created, request)


class SongSubcategoryAdmin(BaseAdmin, model=SongSubcategory):
    name_plural = "Освітні під-категорії"
    category = "Освітний розділ"
    icon = "fa-solid fa-layer-group"

    column_labels = {
        SongSubcategory.title: "Назва під-категорії",
        SongSubcategory.media: "Фото",
        SongSubcategory.main_category: "Категорія",
        SongSubcategory.education_genres: "Жанри",
    }
    column_list = [
        SongSubcategory.title,
        SongSubcategory.media,
        SongSubcategory.main_category,
        SongSubcategory.education_genres,
    ]
    form_columns = [
        SongSubcategory.title,
        SongSubcategory.media,
        SongSubcategory.main_category,
    ]
    column_formatters = {
        SongSubcategory.media: MediaFormatter(),
    }
    form_files_list = [
        SongSubcategory.media,
    ]
    form_args = {
        "main_category": {
            "validators": [DataRequired()],
        },
        "media": {
            "widget": MediaInputWidget(is_required=True),
            "validators": [
                MediaValidator(
                    media_types=IMAGE_TYPES,
                    max_size=MAX_IMAGE_SIZE_MB,
                    is_required=True,
                )
            ],
        },
    }
    column_searchable_list = [
        SongSubcategory.title,
    ]
    form_ajax_refs = {
        "main_category": {
            "fields": ("title",),
            "order_by": "id",
        },
    }

    async def after_model_change(
        self, data: dict, model: Any, is_created: bool, request: Request
    ) -> None:
        await invalidate_cache("get_category", model.main_category_id)
        return await super().after_model_change(data, model, is_created, request)

    async def after_model_delete(self, model: Any, request: Request) -> None:
        await invalidate_cache("get_category", model.main_category_id)
        return await super().after_model_delete(model, request)


class EducationPageSongGenreAdmin(BaseAdmin, model=EducationPageSongGenre):
    name_plural = "Освітні жанри"
    category = "Освітний розділ"
    icon = "fa-solid fa-layer-group"

    column_labels = {
        EducationPageSongGenre.title: "Назва жанру",
        EducationPageSongGenre.sub_category: "Під-категорія",
        EducationPageSongGenre.description: "Опис",
        EducationPageSongGenre.media1: "Фото",
        EducationPageSongGenre.media2: "Фото",
        EducationPageSongGenre.media3: "Фото",
        EducationPageSongGenre.media4: "Фото",
        EducationPageSongGenre.media5: "Фото",
    }
    column_list = [
        EducationPageSongGenre.title,
        EducationPageSongGenre.description,
        EducationPageSongGenre.sub_category,
        EducationPageSongGenre.media1,
    ]
    form_columns = [
        EducationPageSongGenre.title,
        EducationPageSongGenre.sub_category,
        EducationPageSongGenre.description,
        EducationPageSongGenre.media1,
        EducationPageSongGenre.media2,
        EducationPageSongGenre.media3,
        EducationPageSongGenre.media4,
        EducationPageSongGenre.media5,
    ]

    column_formatters = {
        EducationPageSongGenre.description: TextFormatter(
            text_align="left", min_width=250
        ),
        EducationPageSongGenre.media1: PhotoSplitFormatter(EDUCATION_PAGE_PHOTO_FIELDS),
    }
    column_searchable_list = [
        EducationPageSongGenre.title,
    ]
    form_files_list = EDUCATION_PAGE_PHOTO_FIELDS
    form_overrides = {
        "description": TextAreaField,
    }
    form_args = {
        "sub_category": {
            "validators": [DataRequired()],
        },
        "description": {
            "render_kw": {
                "class": "form-control",
                "rows": 7,
                "maxlength": EducationPageSongGenre.description.type.length,
            },
        },
        **{
            field: {
                "widget": MediaInputWidget(is_required=True),
                "validators": [
                    MediaValidator(
                        media_types=IMAGE_TYPES,
                        max_size=MAX_IMAGE_SIZE_MB,
                        is_required=True,
                    )
                ],
            }
            for field in EDUCATION_PAGE_PHOTO_FIELDS[:3]
        },
        **{
            field: {
                "widget": MediaInputWidget(),
                "validators": [
                    MediaValidator(media_types=IMAGE_TYPES, max_size=MAX_IMAGE_SIZE_MB)
                ],
            }
            for field in EDUCATION_PAGE_PHOTO_FIELDS[3:]
        },
    }
    form_ajax_refs = {
        "sub_category": {
            "fields": ("title",),
            "order_by": "title",
        },
    }

    async def on_model_change(
        self, data: dict, model: Any, is_created: bool, request: Request
    ) -> None:
        model.main_category_id = model.sub_category.main_category_id
        return await super().on_model_change(data, model, is_created, request)

    async def after_model_change(
        self, data: dict, model: Any, is_created: bool, request: Request
    ) -> None:
        await invalidate_cache("get_category", model.main_category_id)
        await invalidate_cache("get_genre_info", model.id)
        return await super().after_model_change(data, model, is_created, request)

    async def after_model_delete(self, model: Any, request: Request) -> None:
        await invalidate_cache("get_category", model.main_category_id)
        await invalidate_cache("get_genre_info", model.id)
        return await super().after_model_delete(model, request)
