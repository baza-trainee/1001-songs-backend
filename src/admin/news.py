from typing import Any

from fastapi import Request
from sqladmin import ModelView
from sqladmin.fields import AjaxSelectField, QueryAjaxModelLoader
from wtforms import Form

from src.admin.commons.formatters import (
    format_datetime,
    format_quill,
    format_array_of_string,
)
from src.admin.commons.utils import model_change_for_editor
from src.admin import OurTeamAdmin
from src.news.models import News, NewsCategory
from src.our_team.models import OurTeam


class NewsCategoryAdmin(ModelView, model=NewsCategory):
    is_async = True
    name_plural = "Категорії новин"
    category = "Розділ новин"
    icon = "fa-solid fa-icons"

    can_view_details = True
    can_export = False
    can_create = True

    column_labels = {
        "name": "Назва категорії",
    }
    column_exclude_list = [
        "news",
        "id",
    ]
    form_excluded_columns = ["news"]


class NewsAdmin(ModelView, model=News):
    is_async = True
    name_plural = "Новини"
    category = "Розділ новин"
    icon = "fa-solid fa-kiwi-bird"

    can_view_details = False
    can_export = False
    column_list = [
        News.created_at,
        News.category,
        News.title,
        News.content,
        News.authors,
        News.editors,
        News.photographers,
    ]

    column_labels = {
        News.created_at: "Дата публікації",
        News.category: "Категорія",
        News.title: "Заголовок",
        News.content: "Контент",
        News.authors: "Автор",
        News.editors: "Редактор",
        News.photographers: "Світлини",
    }
    form_columns = [
        News.created_at,
        News.category,
        News.title,
        News.authors,
        News.editors,
        News.photographers,
        News.content,
    ]
    column_formatters = {
        News.created_at: format_datetime,
        News.content: format_quill,
        News.authors: format_array_of_string,
        News.editors: format_array_of_string,
        News.photographers: format_array_of_string,
    }
    # form_overrides = {
    #     News.author : AjaxSelectField
    # }
    # form_args = {
    #     News.author: {
    #         "loader": QueryAjaxModelLoader('full_name', OurTeam, OurTeamAdmin),
    #     },
    # }

    async def scaffold_form(self) -> type[Form]:
        form = await super().scaffold_form()
        form.is_editor_field = [
            "content",
        ]
        del form.content.kwargs["validators"][-1]
        return form

    async def on_model_change(
        self, data: dict, model: Any, is_created: bool, request: Request
    ) -> None:
        await model_change_for_editor(data, model, field_name="content")
        return await super().on_model_change(data, model, is_created, request)
