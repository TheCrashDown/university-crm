import logging
import uuid
from fastapi import APIRouter
from sqlalchemy import insert, select

from lib.models import (
    Classroom,
    Course,
    Event,
    Group,
    GroupCourses,
    UserType,
    User,
    File,
    Task,
)

from routers.pydantic_models import UploadHometaskFrom, UserRegisterForm

from utils.util import Util

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/upload_hometask")
def upload_hometask_endpoint(info: UploadHometaskFrom):
    try:
        r = Util.get_redis_client()
        if not r.exists(info.token) or r.get(info.token) != info.student:
            return {"success": True, "error": "Invalid token"}

        Util.renew_token(r, info.token)

        path = f"/hometasks/{uuid.uuid4()}"
        Util.s3_create(path, info.file)

        with Util.get_session() as session:
            file_id = session.execute(
                insert(File)
                .values(
                    link=path,
                )
                .returning(File.id)
            )

            student_id = session.execute(
                select(User.id).where(User.username == info.student)
            ).first()

            teacher_id = session.execute(
                select(User.id).where(User.username == info.teacher)
            ).first()

            session.execute(
                insert(Task).values(
                    file_id=file_id.scalar(),
                    teacher_id=teacher_id,
                    student_id=student_id,
                )
            )

            session.commit()

        return {"success": True}
    except Exception as err:
        logger.warning(err)
        return {"success": False, "error": str(err)}


@router.post("/student_insert")
def stud_insert(
    user: UserRegisterForm,
):
    with Util.get_session() as session:
        session.execute(
            insert(User).values(
                username=user.username,
                password=user.password,
                firstname=user.firstname,
                surname=user.surname,
                lastname=user.lastname,
                user_type="student",
            )
        )
        session.commit()
    return {"success": True}


@router.get("/Students")
def stud_select():
    with Util.get_session() as session:
        data = session.execute(
            select(
                User.id,
                User.name,
            ).where(UserType.name == "student")
        ).all()

        data = [i._asdict() for i in data]
    return {"success": True, "data": data}


@router.get("/get_events")
def get_student_events_endpoint(token: str):
    try:
        r = Util.get_redis_client()

        username = r.get(token)
        if not username:
            return {"success": False, "error": "Invalid token"}

        Util.renew_token(r, token)

        with Util.get_session() as session:
            data = session.execute(
                select(
                    User.id,
                    Group.name,
                    Event.name,
                    Event.description,
                    Classroom.name,
                    Classroom.location,
                    Event.teacher,
                    Event.start,
                    Event.end,
                )
                .join(Group, Group.id == User.group_id)
                .join(GroupCourses, GroupCourses.course_id == Group.id)
                .join(Course, Course.id == GroupCourses.course_id)
                .join(Event, Event.course == Course.id)
                .join(Classroom, Classroom.id == Event.classroom_id)
                .where(User.username == username)
            ).all()

            data = [i._asdict() for i in data]
        return {"success": True, "data": data}
    except Exception as err:
        logger.warning(err)
        return {"success": False, "error": str(err)}
