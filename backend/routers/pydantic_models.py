"""Pydantic models for API documentation"""

from typing import Optional

from pydantic import BaseModel

class InsertUserForm(BaseModel):
    username: str
    firstname: str
    surname: str
    lastname: Optional[str] = ""

    password: str
    
class InsertUserTypeForm(BaseModel):
    name: str


class InsertQuizForm(BaseModel):
    name: str

class InsertQuizQuestionsForm(BaseModel):
    question: str

class InsertQuizAnswersForm(BaseModel):
    answer: str

