"""Admin panel & debug features"""

from fastapi import APIRouter

from sqlalchemy import insert

from lib.models import create_database
from lib.models import UserType
from utils.util import Util

router = APIRouter()


@router.get("/init_database")
def init_database_endpoint():
    """Initialize database, create tables"""

    try:
        create_database()

        with Util.get_session() as session:
            session.execute(
                insert(UserType).values(
                    [{"id": 1, "name": "teacher"}, {"id": 2, "name": "student"}]
                )
            )
            session.commit()

        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}
