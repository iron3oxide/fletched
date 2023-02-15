from typing import Callable, Type

from fletched.routed_app.view_builder import ViewBuilder


def route(route: str) -> Callable[..., Type[ViewBuilder]]:
    def wrapper(view_builder_class: Type[ViewBuilder]) -> Type[ViewBuilder]:
        view_builder_class.route = route
        return view_builder_class

    return wrapper
