from collections import defaultdict
from typing import Type

import flet as ft

from flet_routed_app.view_builder import ViewBuilder


class RoutedApp:
    def __init__(
        self, page: ft.Page, unauthorized_return_route: str = "/login"
    ) -> None:
        self.page = page
        self.unauthorized_return_route = unauthorized_return_route
        self.route_to_viewbuilder: dict[str, ViewBuilder] = {}
        self.state: defaultdict = defaultdict(lambda: "not set")

        self.page.on_route_change = self.append_view
        self.page.on_view_pop = self.pop_view

    def add_view_builders(self, view_builder_classes: list[Type[ViewBuilder]]) -> None:
        for view_builder_class in view_builder_classes:
            view_builder = view_builder_class(
                page=self.page, unauthorized_return_route=self.unauthorized_return_route
            )
            view_builder.set_app(self)
            if view_builder.route:
                self.route_to_viewbuilder[view_builder.route] = view_builder

    def append_view(self, e: ft.RouteChangeEvent) -> None:
        self.page.views.clear()
        if e.route not in self.route_to_viewbuilder:
            return
        view = self.route_to_viewbuilder[e.route].view_func()
        self.page.views.append(view)
        self.page.update()

    def pop_view(self, e: ft.ViewPopEvent) -> None:
        if len(self.page.views) == 1:
            return
        self.page.views.pop()
        top_view = self.page.views[-1]
        self.page.go(top_view.route)
