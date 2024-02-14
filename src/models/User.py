from pydantic import BaseModel, Field


class User(BaseModel):
    # username: str = Field(default="Undefined", min_length=3, max_length=20)
    # login: str = Field(..., min_length=8)
    # password: str = Field(..., min_length=8)
    username: str = Field()
    login: str = Field()
    password: str = Field()
