from wtforms import TextAreaField
from wtforms.validators import DataRequired

from src.admin.commons.base import BaseAdmin
from src.admin.commons.formatters import (
    MediaFormatter,
    PhotoSplitFormatter,
    TextFormatter,
    format_array_of_string,
    format_quill,
)
from src.admin.commons.utils import MediaInputWidget
from src.admin.commons.validators import MediaValidator, QuillValidator
from src.education.models import (
    EducationPage,
    CalendarAndRitualCategory,
    SongSubcategory,
    EducationPageSongGenre,
)

EDUCATION_PAGE_PHOTO_FIELDS = [
    "media1",
    "media2",
    "media3",
]


class EducationAdmin(BaseAdmin, model=EducationPage):
    category = "Освітний розділ"
    name_plural = "Загальна інформація"
    icon = "fa-solid fa-user-graduate"

    can_create = False
    can_delete = False

    column_labels = {
        EducationPage.title: "Заголовок розділу",
        EducationPage.description: "Опис",
        EducationPage.recommendations: "Рекомендації",
        EducationPage.recommended_sources: "Рекомендовані джерела",
    }
    column_list = column_details_list = form_columns = [
        EducationPage.title,
        EducationPage.description,
        EducationPage.recommendations,
        EducationPage.recommended_sources,
    ]
    column_formatters = {
        EducationPage.description: TextFormatter(text_align="left", min_width=300),
        EducationPage.recommendations: format_quill,
        EducationPage.recommended_sources: format_array_of_string,
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
            "validators": [DataRequired()],
        },
        "title": {
            "validators": [DataRequired()],
        },
        "recommendations": {"validators": [QuillValidator()]},
    }
    form_quill_list = [
        EducationPage.recommendations,
    ]


class CalendarAndRitualCategoryAdmin(BaseAdmin, model=CalendarAndRitualCategory):
    name_plural = "Освітні категорії"
    category = "Освітний розділ"
    icon = "fa-solid fa-layer-group"

    can_create = False
    can_delete = False

    column_list = column_details_list = form_columns = [
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

    column_formatters = {
        CalendarAndRitualCategory.recommended_sources: format_array_of_string,
        CalendarAndRitualCategory.media: MediaFormatter(),
        CalendarAndRitualCategory.description: TextFormatter(
            text_align="left", min_width=250
        ),
    }
    form_files_list = [
        CalendarAndRitualCategory.media,
    ]
    form_overrides = {
        "description": TextAreaField,
    }
    form_args = {
        "title": {
            "validators": [DataRequired()],
        },
        "description": {
            "validators": [DataRequired()],
            "render_kw": {
                "class": "form-control",
                "rows": 7,
                "maxlength": CalendarAndRitualCategory.description.type.length,
            },
        },
        "recommended_sources": {
            "render_kw": {
                "class": "form-control",
                "rows": 7,
            },
        },
        "media": {
            "validators": [MediaValidator()],
            "widget": MediaInputWidget(is_required=True),
        },
    }


class SongSubcategoryAdmin(BaseAdmin, model=SongSubcategory):
    name_plural = "Освітні під-категорії"
    category = "Освітний розділ"
    icon = "fa-solid fa-layer-group"

    column_labels = {
        SongSubcategory.title: "Назва під-категорії",
        SongSubcategory.media: "Фото",
        SongSubcategory.main_category: "Розділ",
        SongSubcategory.education_genres: "Жанри",
    }
    column_list = column_details_list = [
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
            "validators": [MediaValidator(is_required=True)],
            "widget": MediaInputWidget(is_required=True),
        },
    }
    # form_ajax_refs = {
    #     "main_category": {
    #         "fields": ("title",),
    #         "order_by": "id",
    #     },
    # }


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
    }
    column_list = [
        EducationPageSongGenre.title,
        EducationPageSongGenre.description,
        EducationPageSongGenre.sub_category,
        EducationPageSongGenre.media1,
    ]
    form_columns = column_details_list = [
        EducationPageSongGenre.title,
        EducationPageSongGenre.sub_category,
        EducationPageSongGenre.description,
        EducationPageSongGenre.media1,
        EducationPageSongGenre.media2,
        EducationPageSongGenre.media3,
    ]

    column_formatters = {
        EducationPageSongGenre.description: TextFormatter(
            text_align="left", min_width=250
        ),
        EducationPageSongGenre.media1: PhotoSplitFormatter(EDUCATION_PAGE_PHOTO_FIELDS),
    }
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
            "validators": [DataRequired()],
        },
        **{
            field: {
                "validators": [MediaValidator()],
                "widget": MediaInputWidget(),
            }
            for field in EDUCATION_PAGE_PHOTO_FIELDS
        },
    }
    # form_ajax_refs = {
    #     "sub_category": {
    #         "fields": ("title",),
    #         "order_by": "id",
    #     },
    # }
