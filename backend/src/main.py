from sqlalchemy import select
from lib.models import User, GroupCourses, Course, Group, UserType, Group

from utils.util import Util

def get_info(username=str, user_type=str):
    
    with Util.get_session() as session:
        info = session.execute(
            select(
                User.firstname,
                User.surname,
                User.lastname,
            )
            .join(User)
            .where(
                User.username == username,
                UserType.name == user_type,
            )
        ).all()

    return info[0]


def get_courses(username=str):
    engine, session = Util.get_session()

    info = session.execute(
        select(
            Course.name,
        )
        .join(GroupCourses, GroupCourses.id == Group.id)
        .where(Group.id == User.id)
    ).all()

    return info[0]
