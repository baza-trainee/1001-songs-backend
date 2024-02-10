from sqladmin import ModelView

from src.our_team.models import OurTeam


class OurTeamAdmin(ModelView, model=OurTeam):
    name_plural = "Команда"
    icon = "fa-solid fa-people-group"

    column_list = [
        OurTeam.full_name,
        OurTeam.photo,
        OurTeam.description,
    ]
    column_details_exclude_list = ["id"]

    can_edit = True
    can_create = True
    can_delete = True
    can_export = False
