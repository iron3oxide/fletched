from typing import Type

from flet_routed_app.view_builder import ViewBuilder


def login_required(view_builder_class: Type[ViewBuilder]) -> Type[ViewBuilder]:
    def inner(self) -> bool:
        if not self.page.auth:
            return False
        return True

    view_builder_class.auth_func = inner

    return view_builder_class


def group_required(
    view_builder_class: Type[ViewBuilder], group: str
) -> Type[ViewBuilder]:
    def inner(self) -> bool:
        if (
            not self.page.auth
            or not self.page.auth.user
            or group not in self.page.auth.user.groups
        ):
            return False
        return True

    view_builder_class.auth_func = inner

    return view_builder_class
