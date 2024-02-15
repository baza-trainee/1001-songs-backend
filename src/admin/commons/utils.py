import base64
import mimetypes
import re
from typing import Any, Optional

from bs4 import BeautifulSoup
from markupsafe import Markup
from sqladmin.fields import Select2TagsField, QuerySelectField
from sqlalchemy import select
from wtforms import Form, ValidationError, Field, widgets
from src.admin.commons.formatters import MediaFormatter, MediaSplitFormatter

from src.database.database import async_session_maker
from src.config import settings
from src.exceptions import MAX_FIELD_LENTH
from src.utils import delete_photo, generate_file_name, save_photo


class CustomFileInputWidget(widgets.FileInput):
    """
    File input widget with clear checkbox.
    """

    def __init__(
        self, multiple=False, is_file: bool = False, is_required: bool = False
    ):
        super().__init__()
        self.multiple = multiple
        self.is_file = is_file
        self.is_required = is_required

    def __call__(self, field: Field, **kwargs: Any) -> str:
        file_input = super().__call__(field, **kwargs)
        checkbox_id = f"{field.id}_checkbox"
        if self.multiple:
            formatter = MediaSplitFormatter(is_file=self.is_file)
        formatter = MediaFormatter(is_file=self.is_file)
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


async def model_change_for_editor(
    data: dict, model: Any, field_name: str = "content", max_lenth: int = 10000
):
    field_data = data.get(field_name, None)
    if field_data:
        is_clear = False
        soup = BeautifulSoup(data[field_name], "lxml")
        img_tags = soup.find_all("img")
        if img_tags:
            for tag in img_tags:
                pattern_base64 = re.compile(r"data:image/[^;]+;base64")
                if pattern_base64.findall(tag["src"]):
                    base64_data = tag["src"].split(",")[1]
                    binary_data = base64.b64decode(base64_data)
                    image_extension = (
                        mimetypes.guess_extension(
                            tag["src"].split(":")[1].split(";")[0]
                        )
                        or ".png"
                    )
                    image_path = await save_photo(binary_data, model, image_extension)
                    image_url = (
                        f"{settings.BASE_URL}/{image_path}"  # BASE URL FOR DEBUG
                    )
                    tag["src"] = image_url
        else:
            is_clear = True

        span_tags = soup.find_all("span")
        for span_tag in span_tags:
            span_tag.unwrap()
        result = str(soup)
        result_len = len(result)
        if result_len > max_lenth:
            raise ValidationError(
                message=MAX_FIELD_LENTH % (field_name, result_len, max_lenth)
            )
        data[field_name] = result

        model_data = getattr(model, field_name, None)
        if model_data:
            soup_old = BeautifulSoup(model_data, "lxml")
            old_img_tags = soup_old.find_all("img")
            if old_img_tags:
                for img_tag in old_img_tags:
                    if is_clear or img_tag["src"] not in data[field_name]:
                        match = re.search(r"static/(.+)", img_tag["src"])  # FOR DEBUG
                        result = (
                            match.group(0) if match else img_tag["src"]
                        )  # FOR DEBUG
                        await delete_photo(result)


async def model_change_for_files(
    data: dict,
    model: Any,
    is_created: bool,
    fields_name: list[str] = "content",
):
    fields_to_del = []
    for field, field_data in data.items():
        if field in fields_name:
            if field_data.size:
                file_name = generate_file_name(field_data.filename)
                if is_created:
                    data[field].filename = file_name
                else:
                    model_data = getattr(model, field, None)
                    if model_data and model_data != field_data.filename:
                        data[field].filename = file_name
                        await delete_photo(model_data)
            else:
                fields_to_del.append(field)
    for field in fields_to_del:
        del data[field]


class CustomSelect2TagsField(Select2TagsField):
    def __init__(self, model, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = model

    async def __call__(self, **kwargs: object) -> Markup:
        async with async_session_maker() as session:
            query = await session.execute(select(self.model))
            self._select_data = query.scalars().all()
        return super().__call__(**kwargs)
