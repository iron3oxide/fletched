from abc import ABCMeta, abstractmethod

import flet as ft
from pydantic import BaseModel

from fletched.mvp.error import ErrorMessage
from fletched.mvp.protocols import MvpPresenterProtocol


class MvpRenderer(metaclass=ABCMeta):
    ref_map: dict[str, ft.Ref]
    config: BaseModel

    def render(self, model: BaseModel) -> None:
        page: ft.Page | None = None
        model_map = model.dict()

        for variable_name, ref in self.ref_map.items():

            model_field_content = model_map[variable_name]
            control_attribute_name = "value"
            if not hasattr(ref.current, control_attribute_name):
                control_attribute_name = "text"
            if isinstance(model_field_content, ErrorMessage):
                control_attribute_name = "error_text"
                model_field_content = model_field_content.message

            control_attribute_content = getattr(ref.current, control_attribute_name)

            if model_field_content == control_attribute_content:
                continue
            setattr(ref.current, control_attribute_name, model_field_content)

            if not page:
                page = ref.current.page

        if page:
            page.update()

    @abstractmethod
    def build(self, presenter: MvpPresenterProtocol) -> None:
        ...
