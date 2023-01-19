from collections import defaultdict
from typing import Any, ClassVar, Protocol

import flet as ft

from flet_routed_app.state import CustomAppState


class RoutedAppProtocol(Protocol):
    state: ClassVar[defaultdict | CustomAppState]
    page: ft.Page
    unauthorized_return_route: str
    last_unauthorized_route: str | None
    route_to_viewbuilder: dict[str, Any]
