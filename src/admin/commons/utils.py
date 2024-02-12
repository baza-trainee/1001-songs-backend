import base64
import re
from typing import Any

from src.config import settings
from src.utils import delete_photo, generate_file_name, save_photo


# def split_img(content):
#     pattern_base64 = re.compile(r'<div class="quill-image"><img src=".*"></div>')
#     res = pattern_base64.findall(content)
#     if len(res) > 1:
#         fin_res = f'<div class="test">'

#         fin_res += '</div>'


async def model_change_for_editor(data: dict, model: Any, field_name: str = "content"):
    model_data = getattr(model, field_name, None)
    if model_data:
        pattern_base64 = re.compile(
            r'((<p>)?<img src="data:image/[^;]+;base64,)([^"]+)">(</p>)?'
        )
        matches = pattern_base64.findall(data[field_name])
        for img_data in matches:
            header, trash, base64_string, trash = img_data
            image_extension = header.split("/")[1].split(";")[0]
            image_data = base64.b64decode(base64_string)
            image_path = await save_photo(image_data, model, image_extension)
            image_url = (
                f'<img class="quill-image" src="{settings.BASE_URL}/{image_path}">'
            )
            data[field_name] = re.sub(
                pattern_base64, image_url, data[field_name], count=1
            )

        media_folder = model.__tablename__.lower().replace(" ", "_")
        pattern_static = re.compile(
            f'<img class="quill-image" src="[^"]+(/static/media/{media_folder}/[^"]+)">'
        )
        old_data = pattern_static.findall(model_data)
        new_data = pattern_static.findall(data[field_name])
        for file_path in old_data:
            if file_path not in new_data:
                await delete_photo(file_path)


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
