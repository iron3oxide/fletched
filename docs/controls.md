## ModelDataTable

If we want the state of our view to be encapsulated in a model,
the DataTable control (as flet provides it right now) constitutes a challenge
if our data is somewhat dynamic.
It is not easily possible to change the state of a DataTable
as that is encapsulated in possibly thousands of DataCells
that are only accessible via the DataRow they belong to.
Even creating a DataTable is somewhat tedious because of this,
although e.g. [simpledt](https://github.com/StanMathers/simple-datatable)
can mitigate that.
But even if it were way more ergonomic,
our initial problem persists:
We want the state of the DataTable to be external of it,
so we need some kind of data structure outside the control
to dictate what the DataTable displays.

Lucky for us, python has immaculate support for tabular data structures!
You have probably heard of pandas DataFrames,
and they would have been an acceptable choice for our model.
But since performance is very important here
and they are just as ergonomic,
[polars](https://pola-rs.github.io/polars-book/user-guide/introduction.html)
is the DataFrame library we will use.
It allows you to easily create DataFrames
from JSON, Excel, CSV or even SQL statements
(paired with a connection string of course).
Read the details on how to do each [here](https://pola-rs.github.io/polars-book/user-guide/howcani/io/intro.html).

### Usage

#### Config

`ModelDataTable` inherits from `flet.UserControl`,
as all custom controls should prefer to do.
It needs a lot of parameters in order for you to able
to customize as much as possible from the outside.
These parameters have been organized into two Config dataclasses:
`DataTableConfig` for every parameter relating to `flet.DataTable`
and `ModelDataTableConfig` for everything that comes on top and the ref,
because the latter has to be passed to `flet.UserControl.__init__()`.
It also takes a `polars.DataFrame` instance as a parameter
and makes that its initial model.
By default, `ModelDataTable` creates a `flet.DataTable` instance internally
with the given parameters from the `DataTableConfig` instance
and wraps that in a `flet.Row`,
which is then wrapped in a `flet.Column`
that is finally put inside a `flet.Container`.

#### In-table search

If the dataset you want to display doesn't change
and you only need a dynamic table in order to query it,
you can set the `search` field of the `ModelDataTableConfig` instance to True.
This will automatically add a search bar
containing a `flet.Dropdown` with all the columns of the table
and a `flet.TextField` for your search input
with a convenient clear button next to it.

>You can change the default column to search in
>by setting the `search_column_default_index` field in `ModelDataTableConfig`.

You now have a simple but effective and performant "contains" search
for every column of your DataFrame.

Please note that when you set the `model` property
in a `ModelDataTable`,
it is saved as `self._original_model` internally
(which is also the one being returned by the same property).
If `ModelDataTableConfig.search` or `ModelDataTableConfig.create_text_model`
are set to True,
a `self._text_model` is created as well,
which converts all original model columns to `polars.Utf8` strings.
This makes it way easier to search the model
without knowledge of its exact schema
and may aid you when dealing with "truly" dynamic data as well.

#### Examples

Static dataset that needs to be searchable:

```python
import flet as ft
import polars as pl

from fletched.controls import (
    DataTableConfig,
    ModelDataTable,
    ModelDataTableConfig
)


def main(page: ft.Page) -> None:

    model = pl.read_csv(
        file="https://raw.githubusercontent.com/iron3oxide/ndcc/main/ndcc/data/charts.csv",
        infer_schema_length=300,
    )
    dt_config = DataTableConfig(expand=True)
    config = ModelDataTableConfig(search=True)
    table = ModelDataTable(model=model, config=config, dt_config=dt_config)

    page.scroll = ft.ScrollMode.ADAPTIVE
    page.add(table)
    page.update()


ft.app(target=main)
```

Dynamic dataset read from a database,
refreshed on selection change:

```python
import flet as ft
import polars as pl

from fletched.controls import (
    DataTableConfig,
    ModelDataTable,
    ModelDataTableConfig
)

from my_app.settings import settings


def main(page: ft.Page) -> None:
    def get_db_dataframe() -> pl.DataFrame:
        return pl.read_sql(
        sql="SELECT * FROM users;", connection_uri=settings.db_uri
        )
    def refresh_table(e: ft.ControlEvent):
        table.model = get_db_dataframe()

    model = get_db_dataframe()
    dt_config = DataTableConfig(expand=True)
    config = ModelDataTableConfig(on_select_changed_row=refresh_table)
    table = ModelDataTable(model=model, config=config, dt_config=dt_config)

    page.scroll = ft.ScrollMode.ADAPTIVE
    page.add(table)
    page.update()


ft.app(target=main)
```
