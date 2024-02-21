from wtforms import TextAreaField
from wtforms.validators import DataRequired

from src.admin.commons.base import BaseAdmin
from src.admin.commons.formatters import (
    PhotoSplitFormatter,
    MediaFormatter,
    TextFormatter,
    format_array_of_string,
)
from src.admin.commons.utils import CustomSelect2TagsField, MediaInputWidget
from src.admin.commons.validators import MediaValidator
from src.our_team.models import OurTeam
from src.song.models import Genre, Song, Fund

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


class GenreAdmin(BaseAdmin, model=Genre):
    category = "Пісенний розділ"
    name_plural = "Жанри"
    icon = "fa-solid fa-layer-group"

    column_labels = {
        Genre.genre_name: "Назва жанру",
    }
    column_list = form_columns = column_details_list = [
        Genre.genre_name,
    ]
    form_args = {
        "genre_name": {"validators": [DataRequired()]},
    }


class FundAdmin(BaseAdmin, model=Fund):
    category = "Пісенний розділ"
    name_plural = "Фонди"
    icon = "fa-solid fa-layer-group"

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
    form_args = {
        "title": {"validators": [DataRequired()]},
    }


class SongAdmin(BaseAdmin, model=Song):
    category = "Пісенний розділ"
    name_plural = "Пісні"
    icon = "fa-solid fa-music"

    save_as = True

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
        Song.fund: "Фонд",
        Song.recording_date: "Дата",
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
    column_list = [
        Song.title,
        Song.stereo_audio,
        Song.song_text,
        Song.photo1,
        Song.ethnographic_photo1,
        Song.recording_date,
        Song.genres,
        Song.education_genres,
        Song.performers,
        Song.collectors,
        Song.fund,
    ]
    column_details_list = form_columns = [
        Song.title,
        Song.song_text,
        Song.song_descriotion,
        Song.performers,
        Song.city,
        Song.ethnographic_district,
        Song.collectors,
        Song.fund,
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
    column_searchable_list = [
        Song.title,
        Song.song_text,
    ]
    column_sortable_list = [
        Song.recording_date,
    ]
    column_default_sort = ("recording_date", True)
    column_formatters = {
        Song.song_text: TextFormatter(text_align="left", min_width=200),
        Song.collectors: format_array_of_string,
        Song.photo1: PhotoSplitFormatter(PHOTO_FIELDS),
        Song.ethnographic_photo1: PhotoSplitFormatter(ETHNOGRAPHIC_PHOTO_FIELDS),
        Song.stereo_audio: MediaFormatter(file_type="audio"),
    }
    form_files_list = SONG_FIELDS + PHOTO_FIELDS + ETHNOGRAPHIC_PHOTO_FIELDS
    form_overrides = {
        "song_text": TextAreaField,
        "song_descriotion": TextAreaField,
    }
    form_args = {
        "title": {"validators": [DataRequired()]},
        "performers": {"validators": [DataRequired()]},
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
        "genres": {
            "render_kw": {
                "class": "form-control",
                "rows": 20,
            },
            "validators": [DataRequired()],
        },
        "city": {
            "render_kw": {
                "class": "form-control",
                "rows": 20,
            },
            "validators": [DataRequired()],
        },
        **{
            field: {
                "widget": MediaInputWidget(),
                "validators": [
                    MediaValidator(),
                ],
            }
            for field in PHOTO_FIELDS + ETHNOGRAPHIC_PHOTO_FIELDS
        },
        **{
            field: {
                "widget": MediaInputWidget(file_type="audio"),
                "validators": [
                    MediaValidator(file_type="audio"),
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
