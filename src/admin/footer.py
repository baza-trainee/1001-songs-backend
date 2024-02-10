from sqladmin import ModelView

from src.footer.models import Footer


class FooterAdmin(ModelView, model=Footer):
    name_plural = "Футер"
    icon = "fa-solid fa-shoe-prints"

    column_list = [
        Footer.reporting,
        Footer.privacy_policy,
        Footer.rules_and_terms,
        Footer.email,
        Footer.facebook_url,
        Footer.youtube_url,
    ]
    column_details_exclude_list = ["id"]

    can_edit = True
    can_create = True
    can_delete = True
    can_export = False
