from wtforms.validators import DataRequired

from src.admin.commons.base import BaseAdmin
from src.admin.commons.formatters import MediaFormatter, format_quill, ArrayFormatter
from src.admin.commons.utils import MediaInputWidget
from src.admin.commons.validators import MediaValidator
from src.our_project.models import OurProject


class OurProjectAdmin(BaseAdmin, model=OurProject):
    name_plural = "Проєкти"
    icon = "fa-solid fa-hands-holding-circle"
    save_as = True

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
        OurProject.title,
        OurProject.short_description,
        OurProject.preview_photo,
        OurProject.project_date,
        OurProject.location,
        OurProject.authors,
        OurProject.editors,
        OurProject.photographers,
        OurProject.recording,
        OurProject.content,
    ]
    column_list = [
        OurProject.content,
        OurProject.title,
        OurProject.location,
        OurProject.project_date,
        OurProject.short_description,
        OurProject.preview_photo,
        OurProject.authors,
        OurProject.editors,
        OurProject.photographers,
        OurProject.recording,
    ]

    column_formatters = {
        OurProject.content: format_quill,
        OurProject.authors: ArrayFormatter(),
        OurProject.editors: ArrayFormatter(),
        OurProject.photographers: ArrayFormatter(),
        OurProject.recording: ArrayFormatter(),
        OurProject.preview_photo: MediaFormatter(),
    }
    form_quill_list = [
        OurProject.content,
    ]
    form_files_list = [
        OurProject.preview_photo,
    ]
    column_searchable_list = [
        OurProject.title,
    ]
    column_sortable_list = [
        OurProject.project_date,
    ]
    column_default_sort = ("project_date", True)
    form_args = {
        "title": {"validators": [DataRequired()]},
        "short_description": {"validators": [DataRequired()]},
        "location": {"validators": [DataRequired()]},
        "category": {"validators": [DataRequired()]},
        "project_date": {"validators": [DataRequired()]},
        "preview_photo": {
            "widget": MediaInputWidget(is_required=True),
            "validators": [MediaValidator(is_required=True)],
        },
    }
    form_ajax_refs = {
        "location": {
            "fields": ("name",),
            "order_by": "name",
        },
    }
