from datetime import datetime
import logging
import uuid

from fastapi import APIRouter
from sqlalchemy import insert, select, and_
from lib.models import Message, User
from utils.util import Util

from routers.pydantic_models import GetMessagesForm, SendMessageForm

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/get_messages")
def get_messages_endpoint(info: GetMessagesForm):
    r = Util.get_redis_client()
    if not r.exists(info.token):
        return {"success": False, "error": "Invalid token"}
    try:
        with Util.get_session() as session:
            sender = session.execute(
                select(User.username).where(User.id == info.from_id)
            ).first()

            if not sender:
                return {
                    "success": False,
                    "error": f"User with id {info.from_id} wasn't found",
                }

            if not r.get(info.token) == sender.username:
                return {"success": False, "error": "No access to this conversation"}

            receiver = session.execute(
                select(User.username).where(User.id == info.to_id)
            ).first()

            if not receiver:
                return {
                    "success": False,
                    "error": f"User with id {info.to_id} wasn't found",
                }

            messages = session.execute(
                select(Message)
                .where(
                    and_(Message.from_id == info.from_id, Message.to_id == info.to_id)
                )
                .union(
                    select(Message).where(
                        and_(
                            Message.from_id == info.to_id, Message.to_id == info.from_id
                        )
                    )
                )
                .order_by(Message.timestamp)
            ).all()

            messages = [i._as_dict() for i in messages]

        return {"success": True, "messages": messages}

    except Exception as err:
        logger.warning(err)
        return {"success": False, "error": str(err)}


@router.post("/send_message")
def send_message_endpoint(info: SendMessageForm):
    r = Util.get_redis_client()
    if not r.exists(info.token):
        return {"success": False, "error": "Invalid token"}
    try:
        with Util.get_session() as session:
            sender = session.execute(
                select(User.username).where(User.id == info.from_id)
            ).first()

            if not sender:
                return {
                    "success": False,
                    "error": f"User with id {info.from_id} wasn't found",
                }

            if not r.get(info.token) == sender.username:
                return {"success": False, "error": "No access to this conversation"}

            receiver = session.execute(
                select(User.username).where(User.id == info.to_id)
            ).first()

            if not receiver:
                return {
                    "success": False,
                    "error": f"User with id {info.to_id} wasn't found",
                }

            session.execute(
                insert(Message).values(
                    from_id=info.from_id,
                    to_id=info.to_id,
                    content=info.content,
                    timestamp=datetime.now(),
                )
            )
            session.commit()

            return {"success": True}

    except Exception as err:
        logger.warning(err)
        return {"success": False, "error": str(err)}
