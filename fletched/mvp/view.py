from abc import abstractmethod
from dataclasses import asdict, dataclass
from typing import List, Optional, Type

import flet as ft
from abstractcp import Abstract, abstract_class_property
from pydantic import BaseModel

from fletched.mvp.datasource import MvpDataSource
from fletched.mvp.error import ErrorMessage
from fletched.mvp.presenter import MvpPresenter
from fletched.mvp.protocols import MvpPresenterProtocol
from fletched.routed_app import ViewBuilder


@dataclass
class ViewConfig:
    route: Optional[str] = None
    controls: Optional[List[ft.Control]] = None
    appbar: Optional[ft.AppBar] = None
    floating_action_button: Optional[ft.FloatingActionButton] = None
    navigation_bar: Optional[ft.NavigationBar] = None
    vertical_alignment: ft.MainAxisAlignment = ft.MainAxisAlignment.NONE
    horizontal_alignment: ft.CrossAxisAlignment = ft.CrossAxisAlignment.NONE
    spacing: ft.OptionalNumber = None
    padding: ft.PaddingValue = None
    bgcolor: Optional[str] = None
    scroll: Optional[ft.ScrollMode] = None
    auto_scroll: Optional[bool] = None


class MvpView(Abstract, ft.View):
    ref_map = abstract_class_property(dict[str, ft.Ref])
    config = abstract_class_property(ViewConfig)

    def __init__(self) -> None:
        super().__init__(**asdict(self.config))

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


class MvpViewBuilder(ViewBuilder):
    data_source_class: Type[MvpDataSource]
    view_class: Type[MvpView]
    presenter_class: Type[MvpPresenter]

    def build_view(self, route_params: dict[str, str]) -> ft.View:

        if not hasattr(self, "data_source"):
            self.data_source = self.data_source_class(
                app=self.app, route_params=route_params
            )

        self.view_class.config.route = self.route
        self.view: ft.View = self.view_class()
        self.presenter = self.presenter_class(
            data_source=self.data_source,
            view=self.view,
        )
        self.presenter.build()
        self.view.render(self.data_source.current_model)

        return self.view
