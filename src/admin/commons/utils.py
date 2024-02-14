import base64
import mimetypes
import re
from typing import Any

from bs4 import BeautifulSoup
from wtforms import ValidationError

from src.config import settings
from src.exceptions import MAX_FIELD_LENTH
from src.utils import delete_photo, generate_file_name, save_photo


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
