from typing import Any
from fastapi import Request
from src.admin.commons.base import BaseAdmin
from src.admin.commons.formatters import MediaFormatter
from src.admin.commons.utils import MediaInputWidget
from src.admin.commons.validators import MediaValidator
from src.config import DOCUMENT_TYPES, MAX_DOCUMENT_SIZE_MB
from src.database.redis import invalidate_cache
from src.footer.models import Footer

DOCUMENT_FIELDS = ["reporting", "privacy_policy", "rules_and_terms"]


class FooterAdmin(BaseAdmin, model=Footer):
    name_plural = "Футер"
    icon = "fa-solid fa-shoe-prints"
    can_create = False
    can_delete = False

    column_labels = {
        Footer.reporting: "Звітність",
        Footer.privacy_policy: "Політика конфіденційності",
        Footer.rules_and_terms: "Правила користування сайтом",
        Footer.email: "Пошта",
        Footer.facebook_url: "Фейбук",
        Footer.youtube_url: "Ютуб",
    }
    column_exclude_list = column_details_exclude_list = [
        Footer.id,
    ]
    column_formatters = {
        Footer.reporting: MediaFormatter(file_type="document"),
        Footer.privacy_policy: MediaFormatter(file_type="document"),
        Footer.rules_and_terms: MediaFormatter(file_type="document"),
    }
    form_files_list = DOCUMENT_FIELDS
    form_args = {
        field: {
            "widget": MediaInputWidget(file_type="document", is_required=True),
            "validators": [
                MediaValidator(
                    media_types=DOCUMENT_TYPES,
                    max_size=MAX_DOCUMENT_SIZE_MB,
                    is_required=True,
                )
            ],
        }
        for field in DOCUMENT_FIELDS
    }

    async def after_model_change(
        self, data: dict, model: Any, is_created: bool, request: Request
    ) -> None:
        await invalidate_cache("get_footer")
        return await super().after_model_change(data, model, is_created, request)

    async def after_model_delete(self, model: Any, request: Request) -> None:
        await invalidate_cache("get_footer")
        return await super().after_model_delete(model, request)
