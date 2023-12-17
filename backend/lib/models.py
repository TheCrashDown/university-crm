"""Module with ORM models"""

import os

from sqlalchemy import (
    DateTime,
    ForeignKey,
    create_engine,
    UniqueConstraint,
    Column,
    Integer,
    String,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import NullPool


Base = declarative_base()
metadata = Base.metadata


class UserType(Base):
    __tablename__ = "user_type"
    id = Column(Integer, primary_key=True)

    # student, teacher etc.
    name = Column(String, nullable=False)

    __table_args__ = (UniqueConstraint("name", name="unique_user_type_name"),)


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)

    username = Column(String, nullable=False)
    password = Column(String, nullable=False)

    firstname = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    lastname = Column(String)

    type_id = Column(Integer, ForeignKey("user_type.id"), nullable=False)
    group_id = Column(Integer, ForeignKey("group.id"))

    __table_args__ = (UniqueConstraint("username", name="unique_username"),)


class File(Base):
    __tablename__ = "file"
    id = Column(Integer, primary_key=True)

    # link to s3
    link = Column(String, nullable=False)


class Task(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True)

    student_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    file_id = Column(Integer, ForeignKey("file.id"), nullable=False)

    grade = Column(Integer)


class Group(Base):
    __tablename__ = "group"
    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False)


class Course(Base):
    __tablename__ = "course"
    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False)
    lecturer = Column(Integer, ForeignKey("user.id"), nullable=False)


class GroupCourses(Base):
    __tablename__ = "group_courses"
    id = Column(Integer, primary_key=True)

    group_id = Column(Integer, ForeignKey("group.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("course.id"), nullable=False)


class Classroom(Base):
    __tablename__ = "classroom"
    id = Column(Integer, primary_key=True)

    location = Column(String, nullable=False)


class EventType(Base):
    __tablename__ = "event_type"
    id = Column(Integer, primary_key=True)

    # lecture, seminar, general etc.
    name = Column(String, nullable=False)

    __table_args__ = (UniqueConstraint("name", name="unique_event_type_name"),)


class Event(Base):
    __tablename__ = "event"
    id = Column(Integer, primary_key=True)

    name = Column(String)
    description = Column(String)

    type_id = Column(Integer, ForeignKey("event_type.id"), nullable=False)
    classroom_id = Column(Integer, ForeignKey("classroom.id"), nullable=False)
    teacher = Column(Integer, ForeignKey("user.id"), nullable=False)
    course = Column(Integer, ForeignKey("course.id"), nullable=False)

    start = Column(DateTime)
    end = Column(DateTime)

    materials = Column(Integer, ForeignKey("file.id"))
    task = Column(Integer, ForeignKey("file.id"))


class Quiz(Base):
    __tablename__ = "quiz"
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String, nullable=False, unique=True)
    teacher = Column(Integer, ForeignKey("user.id"), nullable=False)

    __table_args__ = (UniqueConstraint("name", name="unique_quiz_name"),)


class QuizQuestions(Base):
    __tablename__ = "quiz_question"
    id = Column(Integer, primary_key=True)
    question = Column(String, nullable=False)
    quiz = Column(Integer, ForeignKey("quiz.id"), nullable=False)


class QuizAnswers(Base):
    __tablename__ = "quiz_answers"
    id = Column(Integer, primary_key=True)
    answer = Column(String)
    quiz = Column(Integer, ForeignKey("quiz_question.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("user.id"), nullable=False)


class Chat(Base):
    __tablename__ = "chat"
    id = Column(Integer, primary_key=True)
    from_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    get_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    message = Column(String)


def create_database():
    """Creating database tables"""
    engine = create_engine(
        os.environ.get("POSTGRES_SECRET"), echo=True, poolclass=NullPool
    )
    Base.metadata.create_all(engine, checkfirst=True)
