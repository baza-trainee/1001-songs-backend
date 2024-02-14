from typing import Any

from fastapi import Request
from sqladmin import ModelView
from wtforms import TextAreaField
from wtforms.validators import DataRequired
from src.admin.commons.formatters import MediaSplitFormatter

from src.admin.commons.utils import model_change_for_files
from src.admin.commons.validators import MediaValidator
from src.song.models import Genre, Song
from src.utils import delete_photo


PHOTO_FIELDS = [
    "photo1",
    "photo2",
    "photo3",
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
    icon = "fa-solid fa-guitar"

    can_edit = True
    can_create = True
    can_export = False

    column_list = [
        Genre.genre_name,
        Genre.songs,
    ]
    column_labels = {
        Genre.genre_name: "Назва жанру",
        Genre.songs: "Пісні",
    }
    form_excluded_columns = [Genre.songs]
    column_details_exclude_list = [Genre.id]


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
        Song.genres,
        Song.education_genres,
        Song.performers,
        Song.collectors,
        Song.archive,
        Song.recording_date,
        Song.photo1,
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
        Song.source: "source",
        Song.recording_date: "Дата запису",
        Song.recording_location: "Місце запису",
        Song.comment_map: "Коментар для карти",
        Song.bibliographic_reference: "bibliographic_reference",
        Song.photo1: "Фото",
        Song.photo2: "Фото 2",
        Song.photo3: "Фото 3",
        Song.video_url: "Посилання на відео",
        Song.stereo_audio: "Пісня",
        Song.multichannel_audio1: "Канал 1",
        Song.multichannel_audio2: "Канал 2",
        Song.multichannel_audio3: "Канал 3",
        Song.multichannel_audio4: "Канал 4",
        Song.multichannel_audio5: "Канал 5",
        Song.multichannel_audio6: "Канал 6",
    }
    column_details_list = [
        Song.title,
        Song.song_text,
        Song.genres,
        Song.performers,
        Song.city,
        Song.ethnographic_district,
        Song.song_descriotion,
        Song.collectors,
        Song.archive,
        Song.source,
        Song.recording_date,
        Song.recording_location,
        Song.bibliographic_reference,
        Song.comment_map,
        Song.photo1,
        Song.photo2,
        Song.photo3,
        Song.video_url,
        Song.stereo_audio,
        Song.multichannel_audio1,
        Song.multichannel_audio2,
        Song.multichannel_audio3,
        Song.multichannel_audio4,
        Song.multichannel_audio5,
        Song.multichannel_audio6,
    ]

    form_columns = [
        Song.title,
        Song.song_text,
        Song.song_descriotion,
        Song.performers,
        Song.city,
        Song.ethnographic_district,
        Song.collectors,
        Song.archive,
        Song.source,
        Song.genres,
        Song.education_genres,
        Song.recording_date,
        Song.recording_location,
        Song.bibliographic_reference,
        Song.comment_map,
        Song.video_url,
        Song.photo1,
        Song.photo2,
        Song.photo3,
        Song.stereo_audio,
        Song.multichannel_audio1,
        Song.multichannel_audio2,
        Song.multichannel_audio3,
        Song.multichannel_audio4,
        Song.multichannel_audio5,
        Song.multichannel_audio6,
    ]
    column_formatters = {
        Song.photo1: MediaSplitFormatter(PHOTO_FIELDS),
    }
    form_overrides = {
        "song_text": TextAreaField,
        "song_descriotion": TextAreaField,
    }
    form_args = {
        #     "title": {"validators": [DataRequired(message="Це поле обов'язкове")]},
        #     "genres": {"validators": [DataRequired(message="Це поле обов'язкове")]},
        #     "city": {"validators": [DataRequired(message="Це поле обов'язкове")]},
        #     "collectors": {"validators": [DataRequired(message="Це поле обов'язкове")]},
        #     "performers": {"validators": [DataRequired(message="Це поле обов'язкове")]},
        #     "ethnographic_district": {"validators": [DataRequired(message="Це поле обов'язкове")]},
        #     "recording_date": {"validators": [DataRequired(message="Це поле обов'язкове")]},
        "song_text": {
            "render_kw": {
                "class": "form-control",
                "rows": 5,
            },
        },
        "song_descriotion": {
            "render_kw": {
                "class": "form-control",
                "rows": 3,
            },
        },
    }

    form_ajax_refs = {
        "genres": {
            "fields": ("genre_name",),
            "order_by": "id",
        },
        "education_genres": {
            "fields": ("title",),
            "order_by": "id",
        },
        "city": {
            "fields": ("name",),
            "order_by": "id",
        },
    }

    async def on_model_change(
        self, data: dict, model: Any, is_created: bool, request: Request
    ) -> None:
        await model_change_for_files(
            data, model, is_created, SONG_FIELDS + PHOTO_FIELDS
        )
        return await super().on_model_change(data, model, is_created, request)

    async def on_model_delete(self, model: Any, request: Request) -> None:
        for field in SONG_FIELDS + PHOTO_FIELDS:
            await delete_photo(getattr(model, field, None))
        return await super().on_model_delete(model, request)
