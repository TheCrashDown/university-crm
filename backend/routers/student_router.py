from fastapi import APIRouter
from sqlalchemy import select, insert

from lib.models import UserType, User
from utils.util import Util

from routers.pydantic_models import InsertUserTypeForm, InsertUserForm

router = APIRouter()


@router.get("/TEST_select")
def TEST_select():
    with Util.get_session() as session:
        data = session.execute(
            select(
                UserType.id,
                UserType.name,
            )
        ).all()

        data = [i._asdict() for i in data]
    return {"success": True, "data": data}


@router.post("/TEST_insert")
def TEST_insert(user_type: InsertUserTypeForm):
    with Util.get_session() as session:
        session.execute(insert(UserType).values(name=user_type.name))
        session.commit()
    return {"success": True}


@router.post("/student_insert")
def stud_insert(user: InsertUserForm, ):
    with Util.get_session() as session:
        session.execute(insert(User).values(username=user.username,
                                            password=user.password,
                                            firstname=user.firstname,
                                            surname=user.surname,
                                            lastname=user.lastname,
                                            user_type='student'))
        session.commit()
    return {"success": True}

@router.get("/Students")
def stud_select():
    with Util.get_session() as session:
        data = session.execute(
            select(
                User.id,
                User.name,
            )
            .where(UserType.name == 'student')
        ).all()

        data = [i._asdict() for i in data]
    return {"success": True, "data": data}
