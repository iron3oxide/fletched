from collections import defaultdict
from typing import Type

import flet as ft
import repath

from flet_routed_app.page_not_found import PageNotFoundView
from flet_routed_app.state import CustomAppState
from flet_routed_app.view_builder import ViewBuilder


class RoutedApp:
    state: defaultdict | CustomAppState

    def __init__(
        self,
        page: ft.Page,
        unauthorized_return_route: str = "/login",
        custom_state: bool = False,
    ) -> None:
        self.page = page
        self.unauthorized_return_route: str = unauthorized_return_route
        self.last_unauthorized_route: str | None = None
        self.route_to_viewbuilder: dict[str, ViewBuilder] = {}

        if not custom_state:
            self.state = defaultdict(lambda: "not set")

        self.page.on_route_change = self._append_view
        self.page.on_view_pop = self._pop_view

    def add_view_builders(self, view_builder_classes: list[Type[ViewBuilder]]) -> None:
        for view_builder_class in view_builder_classes:
            view_builder = view_builder_class(
                page=self.page, unauthorized_return_route=self.unauthorized_return_route
            )
            view_builder._set_app(self)
            if view_builder.route:
                self.route_to_viewbuilder[view_builder.route] = view_builder

    def _append_view(self, e: ft.RouteChangeEvent) -> None:
        self.page.views.clear()
        view = self._get_view(e.route)
        self.page.views.append(view)
        self.page.update()

    def _pop_view(self, e: ft.ViewPopEvent) -> None:
        if len(self.page.views) == 1:
            return
        self.page.views.pop()
        top_view = self.page.views[-1]
        self.page.go(top_view.route)

    def _get_view(self, route: str) -> ft.View:
        template = ft.TemplateRoute(route)
        for route_template, view_builder in self.route_to_viewbuilder.items():
            if template.match(route_template):
                tokens = repath.parse(route_template)
                parameter_names = [
                    token["name"] for token in tokens if isinstance(token, dict)
                ]
                parameters = {
                    parameter_name: getattr(template, parameter_name, "")
                    for parameter_name in parameter_names
                }
                return view_builder.view_func(parameters)
        return PageNotFoundView()
