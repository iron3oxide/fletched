from typing import Type

from flet_routed_app.view_builder import ViewBuilder


def route(route: str):
    def wrapper(view_builder_class: Type[ViewBuilder]) -> Type[ViewBuilder]:
        view_builder_class.route = route
        return view_builder_class

    return wrapper
