from fastapi import APIRouter

from lib.models import UserType, User
from utils.util import Util
from sqlalchemy import select, insert
from routers.pydantic_models import InsertUserTypeForm, InsertUserForm



router = APIRouter()


@router.post("/teacher_insert")
def stud_insert(user: InsertUserForm, ):
    with Util.get_session() as session:
        session.execute(insert(User).values(username=user.username,
                                            password=user.password,
                                            firstname=user.firstname,
                                            surname=user.surname,
                                            lastname=user.lastname,
                                            user_type='teacher'))
        session.commit()
    return {"success": True}

@router.get("/Teachers")
def stud_select():
    with Util.get_session() as session:
        data = session.execute(
            select(
                User.id,
                User.name,
            )
            .where(UserType.name == 'teacher')
        ).all()

        data = [i._asdict() for i in data]
    return {"success": True, "data": data}
  
@router.get("/watch_hometask")
def watch_hometask_endpoint():
    return {"success": True, "data": []}


@router.post("/grade_hometask")
def grade_hometask_endpoint():
    return {"success": True, "data": []}
