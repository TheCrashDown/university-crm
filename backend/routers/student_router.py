from fastapi import APIRouter
from sqlalchemy import select, insert

from lib.models import UserType
from utils.util import Util

from routers.pydantic_models import InsertUserTypeForm

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
