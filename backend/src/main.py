from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from models import User, GroupCourses,  Course, Group, UserType, Group

engine = create_engine('postgresql://user:password@localhost/mydatabase')
Session = sessionmaker(bind=engine)
session = Session()




def get_info(username=str, user_type=str):

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
    
    info = session.execute(
        select(
            Course.name,
        )
        .join(GroupCourses, GroupCourses.id == Group.id)
        .where(
                Group.id == User.id
            )
    ).all()

    return info[0]




