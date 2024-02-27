import base64
import mimetypes
import re
from typing import Literal

from bs4 import BeautifulSoup
from wtforms import ValidationError

from src.config import (
    AUDIO_FORMATS,
    DOCUMENT_FORMATS,
    PHOTO_FORMATS,
    MAX_AUDIO_SIZE_MB,
    MAX_DOCUMENT_SIZE_MB,
    MAX_PHOTO_SIZE_MB,
)
from src.exceptions import DATA_REQUIRED, INVALID_FILE, MAX_FIELD_LENTH, OVERSIZE_FILE
from src.utils import delete_photo, save_photo
from src.config import settings


class MediaValidator:
    def __init__(
        self,
        file_type: Literal["photo", "document", "audio"] = "photo",
        is_required: bool = False,
    ) -> None:
        self.file_type = file_type
        self.is_required = is_required

    def validate_size(self, file_size: int, max_size: int):
        if round(file_size / 1024 / 1024, 2) > max_size:
            raise ValidationError(message=OVERSIZE_FILE % (file_size, max_size))

    def __call__(self, form, field):
        file = field.data
        if file and file.size:
            content_type = file.content_type
            match self.file_type:
                case "photo":
                    if not content_type in PHOTO_FORMATS:
                        raise ValidationError(
                            message=INVALID_FILE % (content_type, PHOTO_FORMATS)
                        )
                    self.validate_size(file.size, MAX_PHOTO_SIZE_MB)
                case "document":
                    if not content_type in DOCUMENT_FORMATS:
                        raise ValidationError(
                            message=INVALID_FILE % (content_type, DOCUMENT_FORMATS)
                        )
                    self.validate_size(file.size, MAX_DOCUMENT_SIZE_MB)
                case "audio":
                    if not content_type in AUDIO_FORMATS:
                        raise ValidationError(
                            message=INVALID_FILE % (content_type, AUDIO_FORMATS)
                        )
                    self.validate_size(file.size, MAX_AUDIO_SIZE_MB)
        else:
            if self.is_required and not form.model_instance:
                raise ValidationError(message=DATA_REQUIRED)


class QuillValidator:
    def __init__(self, max_length: int = 10000) -> None:
        self.max_length = max_length

    def __call__(self, form, field):
        if field.data:
            is_clear = False
            soup = BeautifulSoup(field.data, "lxml")
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
                        image_path = save_photo(
                            binary_data, form.model_instance, image_extension
                        )
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
            if result_len > self.max_length:
                raise ValidationError(
                    message=MAX_FIELD_LENTH % (field.name, result_len, self.max_length)
                )
            field.data = result.replace("'", "&#x27;")
            field.errors = []

            old_data = getattr(form.model_instance, field.name, None)
            if old_data:
                soup_old = BeautifulSoup(old_data, "lxml")
                old_img_tags = soup_old.find_all("img")
                if old_img_tags:
                    for img_tag in old_img_tags:
                        if is_clear or img_tag["src"] not in field.data:
                            match = re.search(
                                r"static/(.+)", img_tag["src"]
                            )  # FOR DEBUG
                            result = (
                                match.group(0) if match else img_tag["src"]
                            )  # FOR DEBUG
                            delete_photo(result)
