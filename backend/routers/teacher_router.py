import logging
from fastapi import APIRouter

from lib.models import Event, UserType, User, Task, File
from utils.util import Util
from sqlalchemy import select, insert, update
from routers.pydantic_models import (
    UpdateEventForm,
    UserRegisterForm,
    WatchHometaskForm,
    GradeHometaskForm,
)


router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/teacher_insert")
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
                user_type="teacher",
            )
        )
        session.commit()
    return {"success": True}


@router.get("/Teachers")
def stud_select():
    with Util.get_session() as session:
        data = session.execute(
            select(
                User.id,
                User.username,
            ).where(UserType.name == "teacher")
        ).all()

        data = [i._asdict() for i in data]
    return {"success": True, "data": data}


@router.get("/watch_hometask")
def watch_hometask_endpoint(info: WatchHometaskForm):
    try:
        r = Util.get_redis_client()
        if not r.exists(info.token) or r.get(info.token) != info.user:
            return {"success": True, "error": "Invalid token"}

        Util.renew_token(r, info.token)

        with Util.get_session() as session:
            task = session.execute(
                select(Task.id, File.link, User.username)
                .join(File, File.id == Task.file_id)
                .join(User, User.id == Task.teacher_id)
            ).first()

            if task.username != info.user:
                return {"success": True, "error": "No access to this task"}

        content = Util.s3_read(task.link)

        return {"success": True, "data": content}
    except Exception as err:
        logger.warning(err)
        return {"success": False, "error": str(err)}


@router.post("/grade_hometask")
def grade_hometask_endpoint(info: GradeHometaskForm):
    try:
        r = Util.get_redis_client()
        if not r.exists(info.token) or r.get(info.token) != info.user:
            return {"success": True, "error": "Invalid token"}

        Util.renew_token(r, info.token)

        with Util.get_session() as session:
            task = session.execute(
                select(Task.id, File.link, User.username)
                .join(File, File.id == Task.file_id)
                .join(User, User.id == Task.teacher_id)
            ).first()

            if task.username != info.user:
                return {"success": True, "error": "No access to this task"}

            session.execute(
                update(Task).where(Task.id == task.id).values(grade=info.grade)
            )
            session.commit()
        return {"success": True}
    except Exception as err:
        logger.warning(err)
        return {"success": False, "error": str(err)}


@router.post("/update_event")
def update_event_endpoint(info: UpdateEventForm):
    try:
        r = Util.get_redis_client()
        if not r.exists(info.token):
            return {"success": True, "error": "Invalid token"}

        with Util.get_session() as session:
            event = session.execute(
                select(Event.id, User.username).join(User, User.id == Event.teacher)
            ).first()

            if event.username != r.get(info.token):
                return {"success": True, "error": "No access to this event"}

            Util.renew_token(r, info.token)

            session.execute(
                update(Event)
                .where(Event.id == event.id)
                .values(
                    name=info.name,
                    teacher=info.teacher,
                    classroom=info.classroom,
                    start=info.start,
                    end=info.end,
                    description=info.description,
                    classroom_id=info.classroom_id,
                    materials=info.materials,
                    task=info.task,
                )
            )
            session.commit()

        return {"success": True}

    except Exception as err:
        logger.warning(err)
        return {"success": False, "error": str(err)}
