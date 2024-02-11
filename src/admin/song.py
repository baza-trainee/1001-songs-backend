from sqladmin import ModelView
from src.song.models import Genre, Song


class GenreAdmin(ModelView, model=Genre):
    icon = "fa-solid fa-guitar"
    column_list = [Genre.genre_name, Genre.songs]
    can_edit = True
    can_create = True
    can_export = False
    category = "Пісенний розділ"
    name_plural = "Жанри"
    column_labels = {
        Genre.genre_name: "Назва жанру",
        Genre.songs: "Пісні",
    }
    form_excluded_columns = [Genre.songs]
    column_details_exclude_list = [Genre.id]


class SongAdmin(ModelView, model=Song):
    icon = "fa-solid fa-music"
    column_list = [
        Song.title,
        Song.genres,
        Song.performers,
        Song.collectors,
        Song.archive,
        Song.recording_date,
    ]
    can_edit = True
    can_create = True
    can_export = False
    category = "Пісенний розділ"
    name_plural = "Пісні"
    column_labels = {
        Song.title: "Назва",
        Song.song_text: "Текст",
        Song.genres: "Жанри",
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
        Song.photo2: "Фото",
        Song.photo3: "Фото",
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
