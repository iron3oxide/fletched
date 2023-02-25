from abc import abstractmethod
from dataclasses import asdict, dataclass
from typing import Any

import flet as ft
from abstractcp import Abstract, abstract_class_property
from pydantic import BaseModel

from fletched.mvp.protocols import MvpPresenterProtocol
from fletched.mvp.renderer import MvpRenderer


@dataclass
class DialogConfig:
    disabled: bool | None = None
    visible: bool | None = None
    data: Any = None
    open: bool = False
    modal: bool = False
    title: ft.Control | None = None
    title_padding: ft.PaddingValue = None
    content_padding: ft.PaddingValue = None
    actions_padding: ft.PaddingValue = None


class MvpDialog(Abstract, ft.UserControl):
    ref_map = abstract_class_property(dict[str, ft.Ref])
    config = abstract_class_property(DialogConfig)

    def __init__(
        self, presenter: MvpPresenterProtocol, ref: ft.Ref | None = None
    ) -> None:
        super().__init__(ref=ref)
        self.dialog = ft.AlertDialog(**asdict(self.config))
        self.presenter = presenter
        self._renderer = MvpRenderer(self.ref_map)

    def build(self) -> ft.AlertDialog:
        self.dialog.content = self.get_content()
        self.dialog.actions = self.get_actions()
        return self.dialog

    @abstractmethod
    def get_content(self) -> ft.Control | None:
        ...

    @abstractmethod
    def get_actions(self) -> list[ft.Control] | None:
        ...

    def render(self, model: BaseModel) -> None:
        self._renderer.render(model)
        if self.page:
            self.update()
