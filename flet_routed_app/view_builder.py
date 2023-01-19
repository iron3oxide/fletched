from abc import ABC, abstractmethod
from typing import Callable, Type

import flet as ft

from flet_routed_app.app_protocol import RoutedAppProtocol


class ViewBuilder(ABC):
    route: str | None = None
    auth_func: Callable[..., bool] | None = None

    def __init__(
        self, *, page: ft.Page, route: str | None = None, unauthorized_return_route: str
    ) -> None:

        self.page: ft.Page = page
        self.unauthorized_return_route = unauthorized_return_route
        if route:
            self.route: str | None = route
        self.__view_func: Callable[..., ft.View] = self.build_view

    @property
    def view_func(self) -> Callable[..., ft.View]:
        if self.auth_func and not self.auth_func():
            self.app.last_unauthorized_route = self.route
            return self._build_unauthorized_view
        return self.__view_func

    @view_func.setter
    def view_func(self, func: Callable) -> None:
        self.__view_func = func

    @abstractmethod
    def build_view(self) -> ft.View:
        ...

    def _set_app(self, app) -> None:
        self.app: RoutedAppProtocol = app

    def _build_unauthorized_view(self) -> ft.View:
        return ft.View(
            controls=[
                ft.TextButton(
                    text="You are not authorized to access this. Click this button to go to the login page.",
                    on_click=lambda e: self.page.go(self.unauthorized_return_route),
                ),
            ],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )


class MvpViewBuilder(ViewBuilder):
    model_class: Type
    view_class: Type
    presenter_class: Type

    def build_view(self) -> ft.View:
        self.model = self.model_class()
        self.view: ft.View = self.view_class(self.route)
        self.presenter = self.presenter_class(
            model=self.model, view=self.view, app=self.app
        )
        self.presenter.build()

        return self.view
