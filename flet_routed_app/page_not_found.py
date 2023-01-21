import flet as ft


class PageNotFoundView(ft.View):
    def __init__(self) -> None:
        vertical_alignment = ft.MainAxisAlignment.CENTER
        horizontal_alignment = ft.CrossAxisAlignment.CENTER
        controls = [ft.Text("Oops! Looks like you took a wrong turn.")]
        super().__init__(
            controls=controls,  # type: ignore
            vertical_alignment=vertical_alignment,
            horizontal_alignment=horizontal_alignment,
        )
