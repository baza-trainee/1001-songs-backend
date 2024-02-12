from wtforms import ValidationError
from src.config import FILE_FORMATS, MAX_FILE_SIZE_MB, PHOTO_FORMATS
from src.exceptions import INVALID_FILE, INVALID_PHOTO, OVERSIZE_FILE


class MediaValidator:
    def __init__(self, is_file: bool = False) -> None:
        self.is_file = is_file

    def __call__(self, form, field):
        file = field.data
        if file and file.size:
            file_size = round(file.size / 1024 / 1024, 2)
            if file_size > MAX_FILE_SIZE_MB:
                raise ValidationError(
                    message=OVERSIZE_FILE % (file_size, MAX_FILE_SIZE_MB)
                )
            if not self.is_file and not file.content_type in PHOTO_FORMATS:
                raise ValidationError(
                    message=INVALID_PHOTO % (file.content_type, PHOTO_FORMATS)
                )
            if self.is_file and not file.content_type in FILE_FORMATS:
                raise ValidationError(
                    message=INVALID_FILE % (file.content_type, FILE_FORMATS)
                )
