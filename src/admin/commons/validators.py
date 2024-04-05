import base64
from datetime import datetime
import mimetypes
import re

from bs4 import BeautifulSoup
from wtforms import ValidationError

from src.exceptions import DATA_REQUIRED, INVALID_FILE, MAX_FIELD_LENTH, OVERSIZE_FILE
from src.utils import delete_photo, save_photo
from src.config import settings


class MediaValidator:
    def __init__(
        self,
        media_types: list,
        max_size: int,
        is_required: bool = False,
    ) -> None:
        self.media_types = media_types
        self.max_size = max_size
        self.is_required = is_required

    def validate_size(self, file_size: int, max_size: int):
        if (file_size := round(file_size / 1024 / 1024, 2)) > max_size:
            raise ValidationError(message=OVERSIZE_FILE % (file_size, max_size))

    def __call__(self, form, field):
        file = field.data
        if file and file.size:
            content_type = file.content_type
            if not content_type in self.media_types:
                raise ValidationError(
                    message=INVALID_FILE % (content_type, self.media_types)
                )
            self.validate_size(file.size, self.max_size)
        else:
            if self.is_required and not form.model_instance:
                raise ValidationError(message=DATA_REQUIRED)


class QuillValidator:
    "max_len with html tags"

    def __init__(self, max_text_len: int = 20000) -> None:
        self.max_text_len = max_text_len

    def __call__(self, form, field):
        def raise_required():
            raise ValidationError("This field is required.")

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
                            binary_data, form.model, image_extension
                        )
                        image_url = (
                            f"{settings.BASE_URL}/{image_path}"  # BASE URL FOR DEBUG
                        )
                        tag["src"] = image_url
            else:
                if field.flags.required and not soup.get_text():
                    raise_required()
                is_clear = True

            span_tags = soup.find_all("span")
            for span_tag in span_tags:
                if "style" not in span_tag.attrs.keys():
                    span_tag.unwrap()
            p_tags = soup.find_all("p")
            separator_class = "quill_p_separator"
            for p_tag in p_tags:
                if (
                    not p_tag.get_text(strip=True)
                    and not p_tag.find_all("img")
                    and not p_tag.find_all("iframe")
                ):
                    if p_tag.next.name == "br":
                        p_tag.next.decompose()
                    p_tag["class"] = separator_class
                elif p_tag.get("class", None):
                    if separator_class in p_tag["class"]:
                        del p_tag["class"]

            result = str(soup)
            if self.max_text_len:
                if (text_len := len(soup.get_text())) > self.max_text_len:
                    raise ValidationError(
                        message=MAX_FIELD_LENTH
                        % (field.name, text_len, self.max_text_len)
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
        elif field.flags.required:
            raise_required()


class PastDateValidator(object):
    def __init__(self, message=None):
        if not message:
            message = "Дата запису має бути в минулому."
        self.message = message

    def __call__(self, form, field):
        if field.data > datetime.today().date():
            raise ValidationError(self.message)


class IntegerLengthValidator(object):
    def __init__(self, min_len: int = 0, max_len: int = None):
        self.min_len = min_len
        self.max_len = max_len

    def __call__(self, form, field):
        if field.data:
            data_len = len(str(field.data))
            if not self.min_len <= data_len <= self.max_len:
                message = "Field must have "
                message += (
                    f"minimum {self.min_len} and maximum {self.max_len}"
                    if self.min_len != self.max_len
                    else f"{self.max_len}"
                )
                message += f" digits. You entered {data_len} digits."
                raise ValidationError(message)


class ArrayStringValidator(object):
    def __init__(self, max_array_len: int = 10, max_string_len: int = 25):
        self.max_array_len = max_array_len
        self.max_string_len = max_string_len

    def __call__(self, form, field):
        message = ""
        if field.data:
            array_len = len(field.data)
            if array_len > self.max_array_len:
                message += f"Field must have {self.max_array_len} items. You entered {array_len} items. "
            for item in field.data:
                data_len = len(item)
                if not data_len <= self.max_string_len:
                    message += f"Items must have maximum {self.max_string_len} characters. You entered {data_len} characters."
                    break
        if message:
            raise ValidationError(message)


class MultipleAjaxValidator(object):
    def __init__(self, max_len: int = 10):
        self.max_len = max_len

    def __call__(self, form, field):
        if field.data:
            array_len = len(field.data)
            if array_len > self.max_len:
                message = f"Field must have {self.max_len} items. You entered {array_len} items."
                raise ValidationError(message)


def validate_url(form, field):
    if field.data:
        if not field.data.startswith(("https://", "http://")):
            message = "URL address is incorrect."
            raise ValidationError(message)


class DependsOnFieldValidator(object):
    def __init__(self, depends_field: str):
        self.depends_field = depends_field

    def __call__(self, form, field):
        file = field.data
        if not file or not file.filename:
            if form.data[self.depends_field]:
                raise ValidationError(message=DATA_REQUIRED)


class OrFieldRequiredValidator(object):
    def __init__(self, second_field: str):
        self.second_field = second_field

    def __call__(self, form, field):
        fields = [field.name, self.second_field]
        if not any([getattr(form, field).data for field in fields]):
            raise ValidationError(
                message=f"Оберіть принаймні одне поле з перелічених: {[getattr(form, field).label.text for field in fields]}"
            )
