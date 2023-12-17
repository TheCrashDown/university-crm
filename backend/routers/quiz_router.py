from fastapi import APIRouter
from sqlalchemy import select, insert

from lib.models import UserType, User, Quiz, QuizQuestions, QuizAnswers
from utils.util import Util

from routers.pydantic_models import (
    InsertQuizForm,
    InsertQuizQuestionsForm,
    InsertQuizAnswersForm,
)


router = APIRouter()


@router.post("/create_quiz")
def quiz_insert(quiz: InsertQuizForm, teacher_name: str):
    with Util.get_session() as session:
        data = session.execute(
            select(
                User.id,
                User.name,
            ).where(
                User.username == teacher_name,
                UserType.name == "teacher",
            )
        ).first()

        session.execute(insert(Quiz).values(name=quiz.name, teacher=data["id"]))
        session.commit()
    return {"success": True}


@router.post("/create_quiz")
def quiz_question_insert(question: QuizQuestions, quiz_name: str):
    with Util.get_session() as session:
        data = session.execute(
            select(
                Quiz.id,
                Quiz.name,
            ).where(
                Quiz.name == quiz_name,
            )
        ).first()

        session.execute(insert(Quiz).values(name=question.question, quiz=data["id"]))
        session.commit()
    return {"success": True}


@router.post("/create_quiz")
def quiz_answer_insert(answer: QuizAnswers, student_name: str, quiz_name: str):
    with Util.get_session() as session:
        data_quiz = session.execute(
            select(
                Quiz.id,
                Quiz.name,
            ).where(
                Quiz.name == quiz_name,
            )
        ).first()

        data_student = session.execute(
            select(
                User.id,
                User.name,
            ).where(
                User.username == student_name,
                UserType.name == "student",
            )
        ).first()

        session.execute(insert(Quiz).values(name=answer.answer))
        session.commit()
    return {"success": True}
