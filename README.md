# Flet Routed App

- [Flet Routed App](#flet-routed-app)
  - [When will I need this?](#when-will-i-need-this)
  - [How do I use this?](#how-do-i-use-this)
    - [ViewBuilder class](#viewbuilder-class)
    - [Route assignment](#route-assignment)
    - [Route protection](#route-protection)
    - [Aggregating ViewBuilder classes](#aggregating-viewbuilder-classes)
    - [RoutedApp usage](#routedapp-usage)
    - [App state](#app-state)
    - [Accessing methods of other views' presenter/controller etc](#accessing-methods-of-other-views-presentercontroller-etc)

## When will I need this?

Say you want to design an app for a government agency with multiple,
let's say 20+ pages (MPA = Multi Page Application).
Since Flet is technically SPA (Single Page Application) only,
you'll use views and some routing to simulate the MPA behaviour.

Not every person in the agency should be able to access every page/view.
Also, they shouldn't be able to see anything
but the login page until they're logged in.
The roles defined in the OAuth token the app receives upon login
will determine what pages/views a user has access to.

You'll probably want to design your app in a way that bundles every page/view
into its own module.
If you used an architecture design pattern
(which you definitely should at this scale),
obtaining the view requires building its model
and presenter or controller as well
and thus you need some function or method to obtain the view.

The way flet routing works ATM,
a view will have to be recreated after a route change,
so you'll want to match each route of your app
to the function or method that creates the appropriate view for it.
You'll also want the function/method to return a different view
or raise an exception if the user is not authorized to access it.
This can create a lot of boilerplate code
if you don't have the help of a library.

## How do I use this?

### ViewBuilder class

In the module of your page/view,
create a file called (something like) `build.py`.
In it, create a class called (something like) `{page_name}ViewBuilder`.
This class should inherit from the `ViewBuilder` class of this library
and at minimum define a method with the signature

```python
def build_view(self) -> flet.View
```

This library also contains convenience ViewBuilder subclasses
that provide a shortcut for common architecture design patterns.
The MvpViewBuilder for example only requires you to define three class variables:

```python
from flet_routed_app import MvpViewBuilder

from my_package.views.counter import CounterModel, CounterPresenter, CounterView


class CounterViewBuilder(MvpViewBuilder):
    model_class = CounterModel
    presenter_class = CounterPresenter
    view_class = CounterView
```

### Route assignment

```python
from flet_routed_app import MvpViewBuilder, route

from my_package.views.counter import CounterModel, CounterPresenter, CounterView


@route("/counter")
class CounterViewBuilder(MvpViewBuilder):
    model_class = CounterModel
    presenter_class = CounterPresenter
    view_class = CounterView
```

### Route protection

```python
from flet_routed_app import MvpViewBuilder, login_required, route

from my_package.views.counter import CounterModel, CounterPresenter, CounterView


@login_required
@route("/counter")
class CounterViewBuilder(MvpViewBuilder):
    model_class = CounterModel
    presenter_class = CounterPresenter
    view_class = CounterView
```

```python
from flet_routed_app import MvpViewBuilder, group_required, route

from my_package.views.counter import CounterModel, CounterPresenter, CounterView


@group_required("demo")
@route("/counter")
class CounterViewBuilder(MvpViewBuilder):
    model_class = CounterModel
    presenter_class = CounterPresenter
    view_class = CounterView
```

### Aggregating ViewBuilder classes

Somewhere in your project, you will have to import all ViewBuilder classes
and aggregate them in a list.
The recommended approach is to do this in the `__init__.py`
of the module that contains all your view modules.

It is also possible to create multiple lists
of different ViewBuilders in different places in your project
and to then add these lists to the app one after another.

### RoutedApp usage

In your main() function,
create an instance of RoutedApp
and add the previously imported list of ViewBuilder classes to the instance.

```python
import flet as ft

from flet_routed_app import RoutedApp

from mypackage import views

def main(page: ft.Page):
    app = RoutedApp(page)
    app.add_view_builders(views.view_builders)

ft.app(target=main)
```

### App state

You can share data between different pages/views
by storing it in the `state` dictionary of the app instance
and retrieving it from there.

`state` is a defaultdict;
if a key does not exist,
it will return the string Literal "not set".

Each ViewBuilder will be passed the app instance
when it is added to that very instance.

### Accessing methods of other views' presenter/controller etc

Though this is not encouraged,
some ViewBuilders (e.g. the MvpViewBuilder)
enable you to access their components
once the corresponding view has been built.
This is possible by getting the respective ViewBuilder object
from within another module using the `app.route_to_view` dictionary
which translates route strings to ViewBuilder objects.
Your typechecker will rightfully complain though
as it does only know that the value is a ViewBuilder,
which doesn't necessarily have a `presenter` attribute for example.

```python
class CounterPresenter:
    def __init__(
        self, *, model: CounterModel, view: CounterViewProtocol, app: RoutedApp
    ) -> None:
        self.model = model
        self.view = view
        self.app = app
        self.page = self.app.page

        self.app.route_to_viewbuilder["/login"].presenter.access_from_app_demo()
```
