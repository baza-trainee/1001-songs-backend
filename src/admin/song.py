from typing import Any

from fastapi import Request
from sqladmin import ModelView
from wtforms import Form, TextAreaField
from wtforms.validators import DataRequired

from src.admin.commons.formatters import (
    MediaSplitFormatter,
    MediaFormatter,
    format_array_of_string,
)
from src.admin.commons.utils import CustomFileInputWidget, model_change_for_files
from src.admin.commons.validators import MediaValidator
from src.song.models import Genre, Song
from src.utils import delete_photo


PHOTO_FIELDS = [
    "photo1",
    "photo2",
    "photo3",
]
ETHNOGRAPHIC_PHOTO_FIELDS = [
    "ethnographic_photo1",
    "ethnographic_photo2",
    "ethnographic_photo3",
]
SONG_FIELDS = [
    "stereo_audio",
    "multichannel_audio1",
    "multichannel_audio2",
    "multichannel_audio3",
    "multichannel_audio4",
    "multichannel_audio5",
    "multichannel_audio6",
]


class GenreAdmin(ModelView, model=Genre):
    is_async = True

    category = "Пісенний розділ"
    name_plural = "Жанри"
    icon = "fa-solid fa-layer-group"

    can_edit = True
    can_create = True
    can_export = False

    column_list = [
        Genre.genre_name,
    ]
    column_labels = {
        Genre.genre_name: "Назва жанру",
    }
    form_excluded_columns = [Genre.songs]
    column_details_exclude_list = [Genre.id]
    form_args = {
        "genre_name": {"validators": [DataRequired()]},
    }


class SongAdmin(ModelView, model=Song):
    is_async = True

    category = "Пісенний розділ"
    name_plural = "Пісні"
    icon = "fa-solid fa-music"

    can_edit = True
    can_create = True
    can_export = False

    column_list = [
        Song.title,
        Song.stereo_audio,
        Song.genres,
        Song.education_genres,
        Song.performers,
        Song.collectors,
        Song.archive,
        Song.recording_date,
        Song.photo1,
        Song.ethnographic_photo1,
    ]
    column_labels = {
        Song.title: "Назва",
        Song.song_text: "Текст",
        Song.genres: "Жанри",
        Song.education_genres: "Жанр освітнього розділу",
        Song.performers: "Виконавці",
        Song.city: "Місто / Поселення",
        Song.ethnographic_district: "Етнографічний регіон",
        Song.song_descriotion: "Опис",
        Song.collectors: "Збирачі",
        Song.archive: "Архів",
        Song.recording_date: "Дата запису",
        Song.recording_location: "Місце запису",
        Song.comment_map: "Коментар для карти",
        Song.photo1: "Фото",
        Song.photo2: "Фото",
        Song.photo3: "Фото",
        Song.ethnographic_photo1: "Етнографічне фото",
        Song.ethnographic_photo2: "Етнографічне фото",
        Song.ethnographic_photo3: "Етнографічне фото",
        Song.video_url: "Посилання на відео",
        Song.stereo_audio: "Пісня",
        Song.multichannel_audio1: "Канал 1",
        Song.multichannel_audio2: "Канал 2",
        Song.multichannel_audio3: "Канал 3",
        Song.multichannel_audio4: "Канал 4",
        Song.multichannel_audio5: "Канал 5",
        Song.multichannel_audio6: "Канал 6",
    }

    column_details_list = form_columns = [
        Song.title,
        Song.song_text,
        Song.song_descriotion,
        Song.performers,
        Song.city,
        Song.ethnographic_district,
        Song.collectors,
        Song.archive,
        Song.genres,
        Song.education_genres,
        Song.recording_date,
        Song.recording_location,
        Song.comment_map,
        Song.video_url,
        Song.photo1,
        Song.photo2,
        Song.photo3,
        Song.ethnographic_photo1,
        Song.ethnographic_photo2,
        Song.ethnographic_photo3,
        Song.stereo_audio,
        Song.multichannel_audio1,
        Song.multichannel_audio2,
        Song.multichannel_audio3,
        Song.multichannel_audio4,
        Song.multichannel_audio5,
        Song.multichannel_audio6,
    ]
    column_formatters = {
        Song.collectors: format_array_of_string,
        Song.photo1: MediaSplitFormatter(PHOTO_FIELDS),
        Song.ethnographic_photo1: MediaSplitFormatter(ETHNOGRAPHIC_PHOTO_FIELDS),
        Song.stereo_audio: MediaFormatter(is_audio=True),
    }
    form_overrides = {
        "song_text": TextAreaField,
        "song_descriotion": TextAreaField,
    }
    form_args = {
        "title": {"validators": [DataRequired()]},
        "performers": {"validators": [DataRequired()]},
        "genres": {"validators": [DataRequired()]},
        "city": {"validators": [DataRequired()]},
        "ethnographic_district": {"validators": [DataRequired()]},
        "recording_date": {"validators": [DataRequired()]},
        "song_text": {
            "render_kw": {
                "class": "form-control",
                "rows": 5,
                "maxlength": Song.song_text.type.length,
            },
        },
        "song_descriotion": {
            "render_kw": {
                "class": "form-control",
                "rows": 3,
                "maxlength": Song.song_descriotion.type.length,
            },
        },
        **{
            field: {
                "widget": CustomFileInputWidget(),
                "validators": [
                    MediaValidator(),
                ],
            }
            for field in PHOTO_FIELDS
        },
        **{
            field: {
                "widget": CustomFileInputWidget(is_audio=True),
                "validators": [
                    MediaValidator(),
                ],
            }
            for field in SONG_FIELDS
        },
    }

    # form_ajax_refs = {
    #     "genres": {
    #         "fields": ("genre_name",),
    #         "order_by": "id",
    #     },
    #     "education_genres": {
    #         "fields": ("title",),
    #         "order_by": "id",
    #     },
    #     "city": {
    #         "fields": ("name",),
    #         "order_by": "id",
    #     },
    # }

    async def scaffold_form(self) -> type[Form]:
        form = await super().scaffold_form()
        # form.city.kwargs["validators"] = form.genres.kwargs["validators"] = [DataRequired()]
        return form

    async def on_model_change(
        self, data: dict, model: Any, is_created: bool, request: Request
    ) -> None:
        await model_change_for_files(
            data,
            model,
            is_created,
            request,
            SONG_FIELDS + PHOTO_FIELDS + ETHNOGRAPHIC_PHOTO_FIELDS,
        )
        return await super().on_model_change(data, model, is_created, request)

    async def on_model_delete(self, model: Any, request: Request) -> None:
        for field in SONG_FIELDS + PHOTO_FIELDS + ETHNOGRAPHIC_PHOTO_FIELDS:
            await delete_photo(getattr(model, field, None))
        return await super().on_model_delete(model, request)
