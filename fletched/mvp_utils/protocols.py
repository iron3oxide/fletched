from typing import Protocol

from pydantic import BaseModel


class MvpPresenterProtocol(Protocol):
    def update_view(self) -> None:
        ...

    def build(self) -> None:
        ...


class MvpViewProtocol(Protocol):
    def render(self, model: BaseModel) -> None:
        ...

    def build(self, presenter: MvpPresenterProtocol) -> None:
        ...
