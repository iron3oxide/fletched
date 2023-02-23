from typing import List, Optional, Type

import flet as ft
from abstractcp import Abstract, abstract_class_property
from pydantic import BaseModel

from fletched.mvp.datasource import MvpDataSource
from fletched.mvp.presenter import MvpPresenter
from fletched.mvp.renderer import MvpRenderer
from fletched.routed_app import PageNotFoundView, ViewBuilder


class ViewConfig(BaseModel):
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

    class Config:
        arbitrary_types_allowed = True


class MvpView(Abstract, MvpRenderer, ft.View):
    ref_map = abstract_class_property(dict[str, ft.Ref])
    config = abstract_class_property(ViewConfig)

    def __init__(self) -> None:
        super().__init__(**self.config.dict())


class MvpViewBuilder(Abstract, ViewBuilder):
    data_source_class = abstract_class_property(Type[MvpDataSource])
    view_class = abstract_class_property(Type[MvpView])
    presenter_class = abstract_class_property(Type[MvpPresenter])

    def build_view(self, route_params: dict[str, str]) -> ft.View:

        if (
            not hasattr(self, "data_source")
            or route_params != self.data_source.route_params
        ):
            self.data_source = self.data_source_class(
                app=self.app, route_params=route_params
            )

        if self.data_source.route_params and not self.data_source.route_params_valid:
            return PageNotFoundView()

        self.view_class.config.route = self.route
        self.view: ft.View = self.view_class()
        self.presenter = self.presenter_class(
            data_source=self.data_source,
            view=self.view,
        )
        self.presenter.build()
        self.view.render(self.data_source.current_model)

        return self.view
