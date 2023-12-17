import logging
import uuid

import bcrypt
from fastapi import APIRouter
from sqlalchemy import insert, select
from lib.models import Group, User, UserType
from utils.util import Util

from routers.pydantic_models import UserLoginForm, UserRegisterForm

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/login")
def login_endpoint(info: UserLoginForm):
    try:
        with Util.get_session() as session:
            user = session.execute(
                select(User).where(User.username == info.username)
            ).first()

            if not user:
                return {"success": False, "error": f"User {info.username} wasn't found"}

            if not bcrypt.checkpw(info.password.encode("utf-8"), info.password):
                return {"success": False, "error": "Wrong password"}

        r = Util.get_redis_client()

        token = str(uuid.uuid4())

        r.set(token, info.username)
        r.expire(token, 3600)

        return {"success": True, "token": token}

    except Exception as err:
        logger.warning(err)
        return {"success": False, "error": str(err)}


@router.get("/register")
def register_endpoint(info: UserRegisterForm):
    try:
        with Util.get_session() as session:
            type_id = session.execute(
                select(UserType.id).where(UserType.name == info.type)
            ).first()

            hashed_password = bcrypt.hashpw(
                info.password.encode("utf-8"), bcrypt.gensalt()
            )

            if not type_id:
                return {"success": False, "error": "Wrong user type"}

            group_id = session.execute(
                select(Group.id).where(Group.name == info.type)
            ).first()

            session.execute(
                insert(User).values(
                    username=info.username,
                    password=hashed_password,
                    firstname=info.firstname,
                    surname=info.surname,
                    lastname=info.lastname,
                    type_id=type_id,
                    group_id=group_id,
                )
            )
            session.commit()

        return {"success": True}
    except Exception as err:
        logger.warning(err)
        return {"success": False, "error": str(err)}
