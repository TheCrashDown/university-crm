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
    teacher_name: str


class InsertQuizQuestionsForm(BaseModel):
    question: str
    quiz_name: str


class InsertQuizAnswersForm(BaseModel):
    answer: str
    student_name: str
    quiz_name: str


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


class UpdateEventForm(BaseModel):
    token: str
    event_id: int

    name: Optional[str] = ""
    teacher: Optional[str] = ""
    classroom: Optional[str] = ""
    start: Optional[str] = ""
    end: Optional[str] = ""
    description: Optional[str] = ""
    classroom_id: Optional[int] = ""
    materials: Optional[str] = ""
    task: Optional[str] = ""
