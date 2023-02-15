from typing import Callable


class Observable:
    def __init__(self) -> None:
        self.observers: list[Callable] = []

    def register(self, fn: Callable) -> None:
        self.observers.append(fn)

    def notify_observers(self) -> None:
        for fn in self.observers:
            fn()
