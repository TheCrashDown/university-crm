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


class InsertQuizForm(BaseModel):
    name: str

class InsertQuizQuestionsForm(BaseModel):
    question: str

class InsertQuizAnswersForm(BaseModel):
    answer: str

class UploadHometaskFrom(BaseModel):
    token: str
    student: str
    teacher: str
    file: bytes


class WatchHometaskForm(BaseModel):
    token: str
    user: str
    task_id: int


class GradeHometaskForm(BaseModel):
    token: str
    teacher: str
    task_id: int
    grade: int
