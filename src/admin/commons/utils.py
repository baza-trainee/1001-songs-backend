import re
from typing import Any, Literal
from markupsafe import Markup

from bs4 import BeautifulSoup
from fastapi import Request
from sqladmin.fields import Select2TagsField
from sqlalchemy import select
from wtforms import Field, widgets

from src.admin.commons.formatters import MediaFormatter
from src.database.database import async_session_maker
from src.utils import delete_photo, generate_file_name


class MediaInputWidget(widgets.FileInput):
    def __init__(
        self,
        file_type: Literal["photo", "document", "audio"] = "photo",
        is_required: bool = False,
    ):
        super().__init__()
        self.file_type = file_type
        self.is_required = is_required

    def __call__(self, field: Field, **kwargs: Any) -> str:
        file_input = super().__call__(field, **kwargs)
        checkbox_id = f"{field.id}_checkbox"
        formatter = MediaFormatter(self.file_type)
        checkbox_label = Markup(
            f'<label class="form-check-label" for="{checkbox_id}">Clear</label>'
        )
        widget_data = formatter(field, "object_data") + file_input
        if not self.is_required:
            checkbox_input = Markup(
                f'<input class="form-check-input" type="checkbox" id="{checkbox_id}" name="{checkbox_id}">'  # noqa: E501
            )
            checkbox = Markup(
                f'<div class="form-check">{checkbox_input}{checkbox_label}</div>'
            )
            widget_data += checkbox
        return widget_data


async def on_model_delete_for_quill(self, model):
    for quil_field in self.form_quill_list:
        model_data = getattr(model, quil_field.name, None)
        if model_data:
            soup_old = BeautifulSoup(model_data, "lxml")
            img_tags = soup_old.find_all("img")
            if img_tags:
                for img_tag in img_tags:
                    match = re.search(r"static/(.+)", img_tag["src"])  # FOR DEBUG
                    result = match.group(0) if match else img_tag["src"]  # FOR DEBUG
                    delete_photo(result)


async def scaffold_form_for_quill(self, form):
    form.quill_list = []
    for quil_field in self.form_quill_list:
        if not isinstance(quil_field, str):
            quil_field = quil_field.name
        form.quill_list.append(quil_field)
    return form


async def on_model_change_for_files(
    self,
    data: dict,
    model: Any,
    is_created: bool,
    request: Request,
):
    fields_name = []
    for field in self.form_files_list:
        if not isinstance(field, str):
            field = field.name
        fields_name.append(field)

    fields_do_not_del = []
    if fields_name:
        for field, field_data in data.items():
            if field in fields_name:
                model_data = getattr(model, field, None)
                if request._form.get(f"{field}_checkbox", None) == "on":
                    delete_photo(model_data)
                    continue
                if field_data.size:
                    file_name = generate_file_name(field_data.filename)
                    if is_created:
                        data[field].filename = file_name
                    else:
                        if model_data and model_data != field_data.filename:
                            data[field].filename = file_name
                            delete_photo(model_data)
                else:
                    fields_do_not_del.append(field)
        for field in fields_do_not_del:
            del data[field]


class CustomSelect2TagsField(Select2TagsField):
    def __init__(self, model, *args, **kwargs):
        self.model = model
        super().__init__(*args, **kwargs)

    async def __call__(self, **kwargs: object) -> Markup:
        async with async_session_maker() as session:
            query = await session.execute(select(self.model))
            self.choices = query.scalars().all()
            self.choices = list(
                set([str(choice) for choice in self.choices] + self.data)
            )
        return super().__call__(**kwargs)
