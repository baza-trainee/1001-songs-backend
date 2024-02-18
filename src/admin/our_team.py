from wtforms import TextAreaField

from src.admin.commons.base import BaseAdmin
from src.admin.commons.formatters import MediaFormatter
from src.admin.commons.utils import MediaInputWidget
from src.admin.commons.validators import MediaValidator
from src.our_team.models import OurTeam


class OurTeamAdmin(BaseAdmin, model=OurTeam):
    name_plural = "Команда"
    category = "Про проєкт"
    icon = "fa-solid fa-people-group"

    column_exclude_list = column_details_exclude_list = [
        OurTeam.id,
    ]

    column_labels = {
        OurTeam.description: "Опис",
        OurTeam.full_name: "Повне ім'я",
        OurTeam.photo: "Фото",
    }
    column_formatters = {
        OurTeam.photo: MediaFormatter(),
    }
    form_files_list = [
        OurTeam.photo,
    ]
    form_overrides = {
        "description": TextAreaField,
    }
    form_args = {
        "description": {
            "render_kw": {
                "class": "form-control",
                "rows": 5,
                "maxlength": OurTeam.description.type.length,
            },
        },
        "photo": {
            "widget": MediaInputWidget(is_required=True),
            "validators": [
                MediaValidator(is_required=True),
            ],
        },
    }
