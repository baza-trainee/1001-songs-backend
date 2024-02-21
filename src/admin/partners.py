from src.admin.commons.base import BaseAdmin
from src.admin.commons.formatters import MediaFormatter
from src.admin.commons.utils import MediaInputWidget
from src.admin.commons.validators import MediaValidator
from src.partners.models import Partners


class PartnersAdmin(BaseAdmin, model=Partners):
    name_plural = "Партнери"
    category = "Про проєкт"
    icon = "fa-solid fa-handshake"

    column_exclude_list = column_details_exclude_list = [
        Partners.id,
    ]

    column_labels = {
        Partners.link: "Посилання",
        Partners.photo: "Фото",
    }
    column_formatters = {
        Partners.photo: MediaFormatter(),
    }
    form_files_list = [
        Partners.photo,
    ]

    form_args = {
        "photo": {
            "widget": MediaInputWidget(is_required=True),
            "validators": [
                MediaValidator(is_required=True),
            ],
        },
    }
