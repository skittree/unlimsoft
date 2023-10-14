from db import Session, User
from models.users import CreateUserModel, GetUsersModel

# можно добавить кастомные exception'ы и ловить их вместо стандартного HTTPException

def get_list(model: GetUsersModel):
    users = Session().query(User)
    if model.min_age is not None:
        users = users.filter(User.age >= model.min_age)
    if model.max_age is not None:
        users = users.filter(User.age <= model.max_age)

    users = users.all()
    return users

def create(model: CreateUserModel):
    user_object = User(**model.dict())
    s = Session()
    s.add(user_object)
    s.commit()
    return user_object