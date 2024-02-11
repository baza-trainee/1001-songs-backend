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
        Song.genres: "Жанри",
        Song.title: "Назва",
        Song.performers: "Виконавці",
        Song.collectors: "Збирачі",
        Song.archive: "Архів",
        Song.recording_date: "Дата запису",
        Song.source: "source",
        Song.bibliographic_reference: "bibliographic_reference",
        Song.researcher_comment: "Коментар",
    }
    column_details_list = [
        Song.title,
        Song.genres,
        Song.performers,
        Song.collectors,
        Song.archive,
        Song.recording_date,
        Song.source,
        Song.bibliographic_reference,
        Song.researcher_comment,
    ]
