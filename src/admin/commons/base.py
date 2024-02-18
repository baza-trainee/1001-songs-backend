from typing import Any, ClassVar, Union

from fastapi import Request
from sqladmin import ModelView
from sqladmin.models import ModelViewMeta
from sqlalchemy import Sequence
from sqlalchemy.orm import InstrumentedAttribute
from wtforms import Form

from src.admin.commons.utils import (
    on_model_change_for_files,
    on_model_delete_for_quill,
    scaffold_form_for_quill,
)
from src.utils import delete_photo

MODEL_ATTR = Union[str, InstrumentedAttribute]


class BaseAdmin(ModelView, metaclass=ModelViewMeta):
    is_async = True

    can_create = True
    can_delete = True
    can_edit = True
    can_view_details = True
    can_export = False

    save_and_another = False
    save_as = False
    save_as_continue = True

    form_files_list: ClassVar[Sequence[MODEL_ATTR]] = []
    form_quill_list: ClassVar[Sequence[MODEL_ATTR]] = []

    model_instance = None

    async def scaffold_form(self) -> type[Form]:
        form = await super().scaffold_form()
        form.model_instance = self.model_instance
        if self.form_quill_list:
            form = await scaffold_form_for_quill(self, form)
        return form

    async def get_object_for_edit(self, value: Any) -> Any:
        self.model_instance = await super().get_object_for_edit(value)
        return self.model_instance

    async def on_model_change(
        self, data: dict, model: Any, is_created: bool, request: Request
    ) -> None:
        await on_model_change_for_files(self, data, model, is_created, request)
        return await super().on_model_change(data, model, is_created, request)

    async def on_model_delete(self, model: Any, request: Request) -> None:
        for field in self.form_files_list:
            if not isinstance(field, str):
                field = field.name
            delete_photo(getattr(model, field, None))

        if self.form_quill_list:
            await on_model_delete_for_quill(self, model)
        return await super().on_model_delete(model, request)
