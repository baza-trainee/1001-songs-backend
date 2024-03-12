from typing import Any

from fastapi import Request
from wtforms import TextAreaField
from wtforms.validators import DataRequired

from src.admin.commons.base import BaseAdmin
from src.admin.commons.exceptions import IMG_REQ
from src.admin.commons.formatters import (
    ArrayFormatter,
    PhotoSplitFormatter,
    MediaFormatter,
    TextFormatter,
)
from src.admin.commons.utils import CustomSelect2TagsField, MediaInputWidget
from src.admin.commons.validators import (
    ArrayStringValidator,
    MediaValidator,
    PastDateValidator,
)
from src.config import AUDIO_TYPES, MAX_AUDIO_SIZE_MB, MAX_IMAGE_SIZE_MB, IMAGE_TYPES
from src.database.redis import invalidate_cache_partial
from src.our_team.models import OurTeam
from src.song.models import Genre, Song, Fund


SONG_PHOTO_RES = (1230, 690)
SONG_ETHNOGRAPHIC_PHOTO_RES = (1024, 1015)
SONG_MAP_PHOTO_RES = (820, 485)

PHOTO_FIELDS = [
    "photo1",
    "photo2",
    "photo3",
    "photo4",
    "photo5",
]
ETHNOGRAPHIC_PHOTO_FIELDS = [
    "ethnographic_photo1",
    "ethnographic_photo2",
    "ethnographic_photo3",
    "ethnographic_photo4",
    "ethnographic_photo5",
]
MAP_FIELDS = [
    "map_photo",
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


class GenreAdmin(BaseAdmin, model=Genre):
    category = "Пісенний розділ"
    name_plural = "Жанри"
    icon = "fa-solid fa-layer-group"
    can_view_details = True

    column_labels = {
        Genre.genre_name: "Назва жанру",
    }
    column_list = form_columns = [
        Genre.genre_name,
    ]
    column_details_list = [
        Genre.genre_name,
        Genre.songs,
    ]

    async def after_model_delete(self, model: Any, request: Request) -> None:
        await invalidate_cache_partial(["filter_songs"])
        return await super().after_model_delete(model, request)


class FundAdmin(BaseAdmin, model=Fund):
    category = "Пісенний розділ"
    name_plural = "Фонди"
    icon = "fa-solid fa-layer-group"
    can_view_details = True

    column_labels = {
        Fund.title: "Назва фонду",
    }
    column_list = form_columns = [
        Fund.title,
    ]
    column_details_list = [
        Fund.title,
        Fund.songs,
    ]


class SongAdmin(BaseAdmin, model=Song):
    category = "Пісенний розділ"
    name_plural = "Пісні"
    icon = "fa-solid fa-music"

    save_as = True
    can_view_details = True

    column_labels = {
        Song.title: "Назва",
        Song.song_text: "Текст",
        Song.genres: "Жанри",
        Song.education_genres: "Жанри освітнього розділу",
        Song.performers: "Виконавці",
        Song.city: "Місто / Поселення",
        Song.ethnographic_district: "Етнографічний регіон",
        Song.song_description: "Інформація",
        Song.collectors: "Збирачі",
        Song.fund: "Фонд",
        Song.is_active: "Активна",
        Song.recording_date: "Дата",
        Song.map_photo: "Карта",
        Song.comment_map: "Коментар для карти",
        Song.photo1: "Фото",
        Song.photo2: "Фото",
        Song.photo3: "Фото",
        Song.photo4: "Фото",
        Song.photo5: "Фото",
        Song.ethnographic_photo1: "Етнографічне фото",
        Song.ethnographic_photo2: "Етнографічне фото",
        Song.ethnographic_photo3: "Етнографічне фото",
        Song.ethnographic_photo4: "Етнографічне фото",
        Song.ethnographic_photo5: "Етнографічне фото",
        Song.video_url: "Посилання на відео",
        Song.stereo_audio: "Пісня",
        Song.multichannel_audio1: "Канал 1",
        Song.multichannel_audio2: "Канал 2",
        Song.multichannel_audio3: "Канал 3",
        Song.multichannel_audio4: "Канал 4",
        Song.multichannel_audio5: "Канал 5",
        Song.multichannel_audio6: "Канал 6",
    }
    column_list = [
        Song.title,
        Song.stereo_audio,
        Song.photo1,
        Song.ethnographic_photo1,
        Song.map_photo,
        Song.recording_date,
        Song.genres,
        Song.education_genres,
        Song.performers,
        Song.collectors,
        Song.fund,
        Song.song_text,
        Song.song_description,
        Song.is_active,
    ]
    column_details_list = form_columns = [
        Song.title,
        Song.song_text,
        Song.song_description,
        Song.performers,
        Song.city,
        Song.ethnographic_district,
        Song.collectors,
        Song.fund,
        Song.genres,
        Song.education_genres,
        Song.recording_date,
        Song.video_url,
        Song.map_photo,
        Song.comment_map,
        Song.photo1,
        Song.photo2,
        Song.photo3,
        Song.photo4,
        Song.photo5,
        Song.ethnographic_photo1,
        Song.ethnographic_photo2,
        Song.ethnographic_photo3,
        Song.ethnographic_photo4,
        Song.ethnographic_photo5,
        Song.stereo_audio,
        Song.multichannel_audio1,
        Song.multichannel_audio2,
        Song.multichannel_audio3,
        Song.multichannel_audio4,
        Song.multichannel_audio5,
        Song.multichannel_audio6,
        Song.is_active,
    ]
    column_searchable_list = [
        Song.title,
        Song.song_text,
    ]
    column_sortable_list = [
        Song.recording_date,
        Song.is_active,
    ]
    column_default_sort = ("recording_date", True)
    column_formatters = {
        Song.song_text: TextFormatter(to_bool=True),
        Song.song_description: TextFormatter(to_bool=True),
        Song.performers: TextFormatter(max_lenth=50),
        Song.collectors: ArrayFormatter(width=150),
        Song.map_photo: MediaFormatter(heigth=80),
        Song.photo1: PhotoSplitFormatter(PHOTO_FIELDS),
        Song.ethnographic_photo1: PhotoSplitFormatter(ETHNOGRAPHIC_PHOTO_FIELDS),
        Song.stereo_audio: MediaFormatter(file_type="audio"),
    }
    form_files_list = (
        SONG_FIELDS + PHOTO_FIELDS + ETHNOGRAPHIC_PHOTO_FIELDS + MAP_FIELDS
    )
    form_overrides = {
        "song_text": TextAreaField,
        "song_description": TextAreaField,
        "collectors": CustomSelect2TagsField,
    }
    form_args = {
        "collectors": {
            "validators": [ArrayStringValidator()],
            "model": OurTeam,
        },
        "recording_date": {"validators": [PastDateValidator()]},
        "song_text": {
            "render_kw": {
                "class": "form-control",
                "rows": 5,
                "maxlength": Song.song_text.type.length,
            },
        },
        "song_description": {
            "render_kw": {
                "class": "form-control",
                "rows": 3,
                "maxlength": Song.song_description.type.length,
            },
        },
        "genres": {
            "validators": [DataRequired()],
        },
        "fund": {
            "validators": [DataRequired()],
        },
        "city": {
            "validators": [DataRequired()],
        },
        PHOTO_FIELDS[0]: {
            "widget": MediaInputWidget(is_required=True),
            "validators": [
                MediaValidator(
                    media_types=IMAGE_TYPES,
                    max_size=MAX_IMAGE_SIZE_MB,
                    is_required=True,
                ),
            ],
            "description": IMG_REQ % SONG_PHOTO_RES,
        },
        ETHNOGRAPHIC_PHOTO_FIELDS[0]: {
            "widget": MediaInputWidget(is_required=True),
            "validators": [
                MediaValidator(
                    media_types=IMAGE_TYPES,
                    max_size=MAX_IMAGE_SIZE_MB,
                    is_required=True,
                ),
            ],
            "description": IMG_REQ % SONG_ETHNOGRAPHIC_PHOTO_RES,
        },
        **{
            field: {
                "widget": MediaInputWidget(),
                "validators": [
                    MediaValidator(media_types=IMAGE_TYPES, max_size=MAX_IMAGE_SIZE_MB),
                ],
                "description": IMG_REQ % SONG_ETHNOGRAPHIC_PHOTO_RES,
            }
            for field in ETHNOGRAPHIC_PHOTO_FIELDS[1:]
        },
        **{
            field: {
                "widget": MediaInputWidget(),
                "validators": [
                    MediaValidator(media_types=IMAGE_TYPES, max_size=MAX_IMAGE_SIZE_MB),
                ],
                "description": IMG_REQ % SONG_PHOTO_RES,
            }
            for field in PHOTO_FIELDS[1:]
        },
        **{
            field: {
                "widget": MediaInputWidget(),
                "validators": [
                    MediaValidator(media_types=IMAGE_TYPES, max_size=MAX_IMAGE_SIZE_MB),
                ],
                "description": IMG_REQ % SONG_MAP_PHOTO_RES,
            }
            for field in MAP_FIELDS
        },
        **{
            field: {
                "widget": MediaInputWidget(file_type="audio"),
                "validators": [
                    MediaValidator(media_types=AUDIO_TYPES, max_size=MAX_AUDIO_SIZE_MB),
                ],
            }
            for field in SONG_FIELDS
        },
    }
    form_ajax_refs = {
        "genres": {
            "fields": ("genre_name",),
            "order_by": "genre_name",
        },
        "education_genres": {
            "fields": ("title",),
            "order_by": "title",
        },
        "city": {
            "fields": ("name",),
            "order_by": "name",
        },
    }
    invalidate_func_list = [
        "get_songs_by_education_genre",
        "filter_song_geotags",
        "filter_songs",
        "get_countries",
        "get_regions",
        "get_cities",
        "get_genres",
        "get_funds",
    ]

    async def after_model_change(
        self, data: dict, model: Any, is_created: bool, request: Request
    ) -> None:
        await invalidate_cache_partial(self.invalidate_func_list)
        return await super().after_model_change(data, model, is_created, request)

    async def after_model_delete(self, model: Any, request: Request) -> None:
        await invalidate_cache_partial(self.invalidate_func_list)
        return await super().after_model_delete(model, request)
