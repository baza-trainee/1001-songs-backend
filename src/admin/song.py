from sqladmin import ModelView
from src.song.models import Genre, Song


class GenreAdmin(ModelView, model=Genre):
    icon = "fa-solid fa-guitar"
    column_list = [Genre.genre_name]
    can_edit = True
    can_create = True
    can_export = False
    category = "Пісенний розділ"
    name_plural = "Жанри"
    column_labels = {Genre.genre_name: "Назва жанру"}
    form_excluded_columns = [Genre.songs]


class SongAdmin(ModelView, model=Song):
    icon = "fa-solid fa-music"
    column_list = [
        Song.title,
        Song.performers,
        Song.collectors,
        Song.source,
        Song.archive,
        Song.recording_date,
    ]
    can_edit = True
    can_create = True
    can_export = False
    category = "Пісенний розділ"
    name_plural = "Пісні"
