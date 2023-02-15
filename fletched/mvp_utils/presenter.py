from dataclasses import dataclass

from fletched.mvp_utils.datasource import MvpDataSource
from fletched.mvp_utils.protocols import MvpViewProtocol


@dataclass
class MvpPresenter:
    data_source: MvpDataSource
    view: MvpViewProtocol

    def __post_init__(self) -> None:
        if self.__class__ == MvpPresenter:
            raise TypeError("Cannot instantiate abstract class.")
        self.data_source.register(self.update_view)

    def build(self) -> None:
        self.view.build(self)

    def update_view(self) -> None:
        self.view.render(self.data_source.current_model)
