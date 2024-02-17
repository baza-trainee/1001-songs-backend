from wtforms.validators import DataRequired

from src.admin.commons.base import BaseAdmin
from src.admin.commons.formatters import (
    MediaFormatter,
    format_quill,
    format_array_of_string,
)
from src.admin.commons.utils import MediaInputWidget
from src.admin.commons.validators import MediaValidator
from src.our_project.models import OurProject


class OurProjectAdmin(BaseAdmin, model=OurProject):
    name_plural = "Проєкти"
    icon = "fa-solid fa-hands-holding-circle"

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
    form_columns = column_details_list = [
        OurProject.content,
        OurProject.title,
        OurProject.short_description,
        OurProject.preview_photo,
        OurProject.project_date,
        OurProject.location,
        OurProject.authors,
        OurProject.editors,
        OurProject.photographers,
        OurProject.recording,
    ]
    column_list = [
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
    form_quill_list = [
        OurProject.content,
    ]
    form_files_list = [
        OurProject.preview_photo,
    ]
    form_args = {
        "title": {"validators": [DataRequired()]},
        "short_description": {"validators": [DataRequired()]},
        "location": {"validators": [DataRequired()]},
        "category": {"validators": [DataRequired()]},
        "content": {"validators": [DataRequired()]},
        "project_date": {"validators": [DataRequired()]},
        "preview_photo": {
            "validators": [MediaValidator()],
            "widget": MediaInputWidget(is_required=True),
        },
    }
