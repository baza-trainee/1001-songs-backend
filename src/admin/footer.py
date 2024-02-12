from typing import Any
from fastapi import Request
from sqladmin import ModelView
from src.admin.commons.utils import model_change_for_files

from src.footer.models import Footer
from src.utils import delete_photo


class FooterAdmin(ModelView, model=Footer):
    is_async = True
    name_plural = "Футер"
    icon = "fa-solid fa-shoe-prints"

    column_exclude_list = [
        Footer.id,
    ]

    column_labels = {
        Footer.reporting: "Звітність",
        Footer.privacy_policy: "Політика конфіденційності",
        Footer.rules_and_terms: "Правила користування сайтом",
        Footer.email: "Пошта",
        Footer.facebook_url: "Фейбук",
        Footer.youtube_url: "Ютуб",
    }

    column_details_exclude_list = ["id"]

    can_edit = True
    can_create = True
    can_delete = True
    can_export = False

    async def on_model_change(
        self, data: dict, model: Any, is_created: bool, request: Request
    ) -> None:
        fields = ["reporting", "privacy_policy", "rules_and_terms"]
        await model_change_for_files(data, model, is_created, fields)
        return await super().on_model_change(data, model, is_created, request)

    async def on_model_delete(self, model: Any, request: Request) -> None:
        fields = ["reporting", "privacy_policy", "rules_and_terms"]
        for field in fields:
            await delete_photo(getattr(model, field, None))
        return await super().on_model_delete(model, request)
