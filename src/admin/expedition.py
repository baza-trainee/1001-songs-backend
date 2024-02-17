from wtforms.validators import DataRequired

from src.admin.commons.base import BaseAdmin
from src.admin.commons.formatters import (
    MediaFormatter,
    TextFormatter,
    format_date,
    format_quill,
    format_array_of_string,
)
from src.admin.commons.utils import CustomSelect2TagsField, MediaInputWidget
from src.admin.commons.validators import MediaValidator, QuillValidator
from src.expedition.models import Expedition
from src.our_team.models import OurTeam

MODEL_TEAM_FIELDS = ["authors", "editors", "photographers", "recording"]


class ExpeditionAdmin(BaseAdmin, model=Expedition):
    name_plural = "Експедиції"
    icon = "fa-solid fa-route"

    column_labels = {
        Expedition.title: "Назва",
        Expedition.short_description: "Короткий опис",
        Expedition.map_photo: "Фото карти",
        Expedition.preview_photo: "Фото прев'ю",
        Expedition.expedition_date: "Дата експедиції",
        Expedition.content: "Контент",
        Expedition.category: "Категорія",
        Expedition.location: "Розташування",
        Expedition.authors: "Збирачі",
        Expedition.editors: "Редактор",
        Expedition.photographers: "Відео-монтаж",
        Expedition.recording: "Запис",
    }

    column_list = [
        Expedition.content,
        Expedition.title,
        Expedition.short_description,
        Expedition.preview_photo,
        Expedition.map_photo,
        Expedition.location,
        Expedition.expedition_date,
        Expedition.category,
        Expedition.authors,
        Expedition.editors,
        Expedition.photographers,
        Expedition.recording,
    ]
    form_columns = column_details_list = [
        Expedition.title,
        Expedition.short_description,
        Expedition.preview_photo,
        Expedition.location,
        Expedition.expedition_date,
        Expedition.map_photo,
        Expedition.category,
        Expedition.authors,
        Expedition.editors,
        Expedition.photographers,
        Expedition.recording,
        Expedition.content,
    ]
    column_formatters = {
        Expedition.short_description: TextFormatter(text_align="left"),
        Expedition.content: format_quill,
        Expedition.authors: format_array_of_string,
        Expedition.editors: format_array_of_string,
        Expedition.photographers: format_array_of_string,
        Expedition.recording: format_array_of_string,
        Expedition.map_photo: MediaFormatter(),
        Expedition.preview_photo: MediaFormatter(),
        Expedition.expedition_date: format_date,
    }
    column_searchable_list = [
        Expedition.title,
    ]
    column_sortable_list = [Expedition.expedition_date]
    column_default_sort = ("expedition_date", True)
    form_files_list = [
        Expedition.preview_photo,
        Expedition.map_photo,
    ]
    form_quill_list = [
        Expedition.content,
    ]
    form_overrides = {
        **{field: CustomSelect2TagsField for field in MODEL_TEAM_FIELDS},
    }
    form_args = {
        "category": {"validators": [DataRequired()]},
        "location": {"validators": [DataRequired()]},
        "expedition_date": {"validators": [DataRequired()]},
        "content": {"validators": [QuillValidator()]},
        "map_photo": {
            "widget": MediaInputWidget(is_required=True),
            "validators": [MediaValidator(is_required=True)],
        },
        "preview_photo": {
            "widget": MediaInputWidget(is_required=True),
            "validators": [MediaValidator(is_required=True)],
        },
        **{field: {"model": OurTeam} for field in MODEL_TEAM_FIELDS},
    }
