from pydantic import BaseModel


class MvpModel(BaseModel):
    class Config:
        allow_mutation = False
        arbitrary_types_allowed = True

    pass
