import os
from typing import Any
from fastapi import Request
from sqladmin import ModelView
from wtforms import FileField
from src.education.models import EducationSection
from src.utils import save_photo


class EducationAdmin(ModelView, model=EducationSection):
    column_list = [
        EducationSection.title,
        EducationSection.description,
        EducationSection.media1,
        EducationSection.media2,
        EducationSection.media3,
        EducationSection.media4,
        EducationSection.media5,
    ]
    column_details_exclude_list = ["id"]

    can_edit = True
    can_create = True
    can_delete = True
    can_export = False

    form_overrides = {
        "media1": FileField,
        "media2": FileField,
        "media3": FileField,
        "media4": FileField,
        "media5": FileField,
    }

    async def on_model_change(
        self, data: dict, model: Any, is_created: bool, request: Request
    ) -> None:
        for field in ["media1", "media2", "media3", "media4", "media5"]:
            if data[field] and getattr(model, field) != data[field]:
                upload_file = data.pop(field)
                filename = os.path.join("static", upload_file.filename)
                await save_photo(upload_file, model)
                data[field] = filename
        return await super().on_model_change(data, model, is_created, request)
