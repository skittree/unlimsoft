from db import User
from models.users import CreateUserModel, GetUsersModel

# можно добавить кастомные exception'ы и ловить их вместо стандартного HTTPException

def get_list(session, model: GetUsersModel):
    users = session.query(User)
    if model.min_age is not None:
        users = users.filter(User.age >= model.min_age)
    if model.max_age is not None:
        users = users.filter(User.age <= model.max_age)

    users = users.all()
    return users

def create(session, model: CreateUserModel):
    user_object = User(**model.dict())
    session.add(user_object)
    session.commit()
    return user_object