from pydantic import BaseModel


class MvpModel(BaseModel):
    class Config:
        allow_mutation = False
        smart_union = True
        # arbitrary_types_allowed = True
