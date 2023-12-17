from fastapi import APIRouter

from lib.models import UserType, User

from routers.pydantic_models import InsertUserTypeForm, InsertUserForm

from utils.util import Util

router = APIRouter()


@router.post("/upload_hometask")
def upload_hometask_endpoint():
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
