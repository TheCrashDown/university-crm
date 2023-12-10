from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Task,  Course, Event, UserType

engine = create_engine('postgresql://user:password@localhost/mydatabase')
Session = sessionmaker(bind=engine)
session = Session()



def get_info(username=dict, user_type=str):

    user_type = session.query(UserType).filter(UserType.name == user_type).first()
    user = session.query(User).filter(User.username == username, User.type_id == user_type).first()
    return dict([user.name, user.lastname, user.surname])


