from dataclasses import dataclass
from typing import Self


@dataclass
class ErrorMessage:
    message: str

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v) -> Self:
        if not isinstance(v, cls):
            raise TypeError("not an instance of ErrorMessage")
        return v
