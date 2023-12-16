"""Pydantic models for API documentation"""

from typing import Optional

from pydantic import BaseModel


class UserRegisterForm(BaseModel):
    username: str
    password: str
    firstname: str
    surname: str
    lastname: Optional[str] = ""

    type: str
    group: Optional[str] = ""

class UserLoginForm(BaseModel):
    username: str
    password: str


class InsertUserTypeForm(BaseModel):
    name: str
