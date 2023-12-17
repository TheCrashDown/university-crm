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
def quiz_insert(quiz: InsertQuizForm):
    with Util.get_session() as session:
        data = session.execute(
            select(
                User.id,
                User.name,
            ).where(
                User.username == quiz.teacher_name,
                UserType.name == "teacher",
            )
        ).first()

        session.execute(insert(Quiz).values(name=quiz.name, teacher=data["id"]))
        session.commit()
    return {"success": True}


@router.post("/create_quiz")
def quiz_question_insert(question: InsertQuizQuestionsForm):
    with Util.get_session() as session:
        data = session.execute(
            select(
                Quiz.id,
                Quiz.name,
            ).where(
                Quiz.name == question.quiz_name,
            )
        ).first()

        session.execute(insert(Quiz).values(name=question.question, quiz=data["id"]))
        session.commit()
    return {"success": True}


@router.post("/create_quiz")
def quiz_answer_insert(info: InsertQuizAnswersForm):
    with Util.get_session() as session:
        data_quiz = session.execute(
            select(
                Quiz.id,
                Quiz.name,
            ).where(
                Quiz.name == info.quiz_name,
            )
        ).first()

        data_student = session.execute(
            select(
                User.id,
                User.name,
            ).where(
                User.username == info.student_name,
                UserType.name == "student",
            )
        ).first()

        session.execute(
            insert(QuizAnswers).values(
                answer=info.answer,
                quiz=data_quiz["id"],
                student_id=data_student["id"],
            )
        )
        session.commit()
    return {"success": True}
