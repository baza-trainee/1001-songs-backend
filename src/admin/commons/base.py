from typing import Any, ClassVar, Union

from fastapi import HTTPException, Request, Response
from fastapi.responses import JSONResponse
from sqladmin import BaseView, ModelView, expose
from sqladmin.models import ModelViewMeta
from sqladmin.ajax import QueryAjaxModelLoader
from sqlalchemy import Sequence
from sqlalchemy.orm import InstrumentedAttribute
from wtforms import Form

from src.admin.commons.utils import (
    CustomAjaxSelect2Widget,
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
    can_view_details = False
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
        for file_key in self.form_files_list:
            if not isinstance(file_key, str):
                file_key = file_key.name
            field_class = getattr(form, file_key).field_class
            field_class.model_data = getattr(self.model_instance, file_key, None)
        for ajax_key in self.form_ajax_refs.keys():
            field_class = getattr(form, ajax_key).field_class
            field_class.widget = CustomAjaxSelect2Widget(field_class.widget.multiple)
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


class CustomAjaxAdmin(BaseView):
    name = "custom_ajax"

    def is_visible(self, request: Request) -> bool:
        return False

    @expose("/{identity}/ajax/new_lookup")
    async def ajax_lookup(self, request: Request) -> Response:
        """Ajax lookup route."""

        identity = request.path_params["identity"]
        model_view = self._admin_ref._find_model_view(identity)

        name = request.query_params.get("name")
        term = request.query_params.get("term", None)

        if term:
            term = term.strip()
        else:
            term = ""

        if not name:
            raise HTTPException(status_code=400)

        try:
            loader: QueryAjaxModelLoader = model_view._form_ajax_refs[name]
        except KeyError:
            raise HTTPException(status_code=400)

        data = [loader.format(m) for m in await loader.get_list(term, limit=100)]
        return JSONResponse({"results": data})
