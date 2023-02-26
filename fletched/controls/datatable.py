from dataclasses import asdict, dataclass
from typing import Any, Callable, Optional, Union

import flet as ft
import polars as pl
from flet_core.gradients import Gradient
from flet_core.types import (
    AnimationValue,
    BorderRadiusValue,
    OffsetValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)


@dataclass
class DataTableConfig:
    width: ft.OptionalNumber = None
    height: ft.OptionalNumber = None
    left: ft.OptionalNumber = None
    top: ft.OptionalNumber = None
    right: ft.OptionalNumber = None
    bottom: ft.OptionalNumber = None
    expand: Union[None, bool, int] = None
    col: Optional[ResponsiveNumber] = None
    opacity: ft.OptionalNumber = None
    rotate: RotateValue = None
    scale: ScaleValue = None
    offset: OffsetValue = None
    aspect_ratio: ft.OptionalNumber = None
    animate_opacity: AnimationValue = None
    animate_size: AnimationValue = None
    animate_position: AnimationValue = None
    animate_rotation: AnimationValue = None
    animate_scale: AnimationValue = None
    animate_offset: AnimationValue = None
    on_animation_end = None
    tooltip: Optional[str] = None
    visible: Optional[bool] = None
    disabled: Optional[bool] = None
    data: Any = None
    border: Optional[ft.Border] = None
    border_radius: BorderRadiusValue = None
    horizontal_lines: Optional[ft.BorderSide] = None
    vertical_lines: Optional[ft.BorderSide] = None
    checkbox_horizontal_margin: ft.OptionalNumber = None
    column_spacing: ft.OptionalNumber = None
    data_row_color: Union[None, str, dict[ft.MaterialState, str]] = None
    data_row_height: ft.OptionalNumber = None
    data_text_style: Optional[ft.TextStyle] = None
    bgcolor: Optional[str] = None
    gradient: Optional[Gradient] = None
    divider_thickness: ft.OptionalNumber = None
    heading_row_color: Union[None, str, dict[ft.MaterialState, str]] = None
    heading_row_height: ft.OptionalNumber = None
    heading_text_style: Optional[ft.TextStyle] = None
    horizontal_margin: ft.OptionalNumber = None
    show_bottom_border: Optional[bool] = None
    show_checkbox_column: Optional[bool] = None
    sort_ascending: Optional[bool] = None
    sort_column_index: Optional[int] = None
    on_select_all = None


@dataclass
class ModelDataTableConfig:
    ref: ft.Ref | None = None
    search: bool = False
    search_column_default_index: int = 0
    create_text_model: bool = False
    # row callbacks
    on_select_changed_row: Callable | None = None
    on_long_press_row: Callable | None = None
    # cell callbacks
    on_long_press_cell: Callable | None = None
    on_tap_cell: Callable | None = None
    on_double_tap_cell: Callable | None = None
    on_tap_cancel_cell: Callable | None = None
    on_tap_down_cell: Callable | None = None
    # column callbacks
    on_sort_column: Callable | None = None


class ModelDataTable(ft.UserControl):
    def __init__(
        self,
        *,
        model: pl.DataFrame,
        config: ModelDataTableConfig = ModelDataTableConfig(),
        dt_config: DataTableConfig = DataTableConfig(),
    ) -> None:
        super().__init__(ref=config.ref)
        self.data_table = ft.DataTable(**asdict(dt_config))
        self.config = config
        self.model = model
        if config.search:
            self._setup_search_bar()

    @property
    def model(self) -> pl.DataFrame:
        return self._original_model

    @model.setter
    def model(self, model: pl.DataFrame) -> None:
        self._original_model = model
        self.render_model(self._original_model)
        if self.config.create_text_model or self.config.search:
            self._text_model = model.with_columns(pl.col("*").cast(pl.Utf8))

    def build(self) -> ft.Container:
        scroll = ft.ScrollMode.ADAPTIVE if not self.data_table.expand else None
        controls: list[ft.Control] = [
            ft.Row(
                [self.data_table],
                scroll=scroll,
            )
        ]
        if self.config.search:
            controls.insert(0, self.search_bar)
        return ft.Container(ft.Column(controls), border=ft.border.all(2))

    def render_model(self, model: pl.DataFrame) -> None:
        self.data_table.columns = [
            ft.DataColumn(ft.Text(column), on_sort=self.config.on_sort_column)
            for column in model.columns
        ]
        self.data_table.rows = [
            ft.DataRow(
                [self._get_cell(cell) for cell in row],
                on_select_changed=self.config.on_select_changed_row,
                on_long_press=self.config.on_long_press_row,
            )
            for row in model.rows()
        ]
        if self.page:
            self.update()

    def _get_cell(self, text: str) -> ft.DataCell:
        return ft.DataCell(
            ft.Text(text),
            on_long_press=self.config.on_long_press_cell,
            on_tap=self.config.on_tap_cell,
            on_double_tap=self.config.on_double_tap_cell,
            on_tap_cancel=self.config.on_tap_cancel_cell,
            on_tap_down=self.config.on_tap_down_cell,
        )

    def _setup_search_bar(self) -> None:
        self.search_field = self._get_search_field()
        self.column_dropdown = self._get_column_dropdown()
        self.search_bar = ft.Container(
            ft.Row(
                [
                    self.column_dropdown,
                    self.search_field,
                ],
            ),
            padding=ft.padding.all(10.0),
        )

    def _get_column_dropdown(self) -> ft.Dropdown:
        options = [
            ft.dropdown.Option(column_name, column_name)
            for column_name in self._text_model.columns
        ]
        return ft.Dropdown(
            options=options,
            value=str(options[self.config.search_column_default_index].key),
        )

    def _get_search_field(self) -> ft.Container:
        def clear(e: ft.ControlEvent) -> None:
            search_field.value = ""
            if self.page:
                self.render_model(self._text_model)
                search_field.focus()

        search_field = ft.TextField(expand=True, on_change=self._filter_model)
        clear_button = ft.IconButton(ft.icons.HIGHLIGHT_REMOVE, on_click=clear)
        return ft.Container(ft.Row([search_field, clear_button]), expand=True)

    def _filter_model(self, e: ft.ControlEvent) -> None:
        query = e.control.value
        if not query:
            self.render_model(self._text_model)
            return
        filtered_model = self._text_model.filter(
            pl.col(str(self.column_dropdown.value)).str.contains(query, literal=True)
        )
        self.render_model(filtered_model)


def main(page: ft.Page) -> None:

    model = pl.read_csv(
        file="https://raw.githubusercontent.com/iron3oxide/ndcc/main/ndcc/data/charts.csv",
        infer_schema_length=300,
    )
    parent_config = DataTableConfig(expand=True)
    config = ModelDataTableConfig(
        search=True,
        search_column_default_index=1,
    )
    table = ModelDataTable(model=model, config=config, dt_config=parent_config)
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.add(table)
    page.update()


ft.app(target=main)
