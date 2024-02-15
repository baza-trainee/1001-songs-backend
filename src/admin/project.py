from typing import Any

from fastapi import Request
from sqladmin import ModelView
from wtforms import Form
from wtforms.validators import DataRequired

from src.admin.commons.formatters import (
    MediaFormatter,
    format_quill,
    format_array_of_string,
)
from src.admin.commons.utils import model_change_for_editor
from src.our_project.models import OurProject


class OurProjectAdmin(ModelView, model=OurProject):
    is_async = True

    name_plural = "Проєкти"
    icon = "fa-solid fa-hands-holding-circle"

    can_view_details = True
    can_export = False
    can_create = True

    column_list = form_columns = [
        OurProject.title,
        OurProject.location,
        OurProject.project_date,
        OurProject.short_description,
        OurProject.preview_photo,
        OurProject.content,
        OurProject.authors,
        OurProject.editors,
        OurProject.photographers,
        OurProject.recording,
    ]
    column_labels = {
        OurProject.title: "Назва",
        OurProject.short_description: "Короткий опис",
        OurProject.location: "Локація",
        OurProject.content: "Контент",
        OurProject.project_date: "Дата",
        OurProject.preview_photo: "Фото прев'ю",
        OurProject.authors: "Автори",
        OurProject.editors: "Редактори",
        OurProject.photographers: "Світлини",
        OurProject.recording: "Запис",
    }
    column_details_list = [
        OurProject.title,
        OurProject.location,
        OurProject.project_date,
        OurProject.short_description,
        OurProject.preview_photo,
        OurProject.content,
        OurProject.authors,
        OurProject.editors,
        OurProject.photographers,
        OurProject.recording,
    ]
    column_formatters = {
        OurProject.content: format_quill,
        OurProject.authors: format_array_of_string,
        OurProject.editors: format_array_of_string,
        OurProject.photographers: format_array_of_string,
        OurProject.recording: format_array_of_string,
        OurProject.preview_photo: MediaFormatter(),
    }
    form_args = {
        "title": {"validators": [DataRequired(message="Це поле обов'язкове")]},
        "short_description": {
            "validators": [DataRequired(message="Це поле обов'язкове")]
        },
        "location": {"validators": [DataRequired(message="Це поле обов'язкове")]},
        "category": {"validators": [DataRequired(message="Це поле обов'язкове")]},
        "content": {"validators": [DataRequired(message="Це поле обов'язкове")]},
        "project_date": {"validators": [DataRequired(message="Це поле обов'язкове")]},
        "preview_photo": {"validators": [DataRequired(message="Це поле обов'язкове")]},
    }

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
