from datetime import datetime

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username: str
    password: str


class CreateUser(UserBase):
    pass


class User(BaseModel):
    id: int
    username: str
    email: str
    reg_date: datetime
    is_admin: bool = Field(default=False, alias="is_admin")

    class Config:
        from_attributes = True
