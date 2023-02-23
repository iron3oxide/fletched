from typing import Any

import flet as ft
from abstractcp import Abstract, abstract_class_property
from pydantic import BaseModel

from fletched.mvp.renderer import MvpRenderer


class DialogConfig(BaseModel):
    ref: ft.Ref | None = None
    disabled: bool | None = None
    visible: bool | None = None
    data: Any = None
    open: bool = False
    modal: bool = False
    title: ft.Control | None = None
    title_padding: ft.PaddingValue = None
    content: ft.Control | None = None
    content_padding: ft.PaddingValue = None
    actions: list[ft.Control] | None = None
    actions_padding: ft.PaddingValue = None

    class Config:
        arbitrary_types_allowed = True


class MvpDialog(Abstract, MvpRenderer, ft.AlertDialog):
    ref_map = abstract_class_property(dict[str, ft.Ref])
    config = abstract_class_property(DialogConfig)

    def __init__(self) -> None:
        super().__init__(**self.config.dict())
