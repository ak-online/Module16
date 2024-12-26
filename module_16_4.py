from typing import List, Annotated

from fastapi import FastAPI, Path, HTTPException
from pydantic import BaseModel

app = FastAPI()

users = []


class User(BaseModel):
    id: int = None
    username: str
    age: int


@app.get("/users")
async def get_all_users() -> List[User]:
    # print("LEN USERS ", len(users))
    # print('ID ',users[len(users) - 1].id)
    return users


@app.post("/user/{username}/{age}")
async def create_user(user: User,
                      username: Annotated[
                          str, Path(min_length=5, max_length=20, description='Enter username', example="UrbanUser")],
                      age: Annotated[int, Path(ge=18, le=120, description='Enter age', example=22)]) -> str:
    if len(users) == 0:
        user.id = 1
    else:
        user.id = users[len(users) - 1].id + 1
    user.username = username
    user.age = age
    users.append(user)
    return (f"User {username}, age - {age} is created. User.ID - {user.id} ")


@app.put('/user/{user_id}/{username}/{age}')
async def update_users(user_id: int = Path(ge=1, le=100, description='Enter User ID'),
                       username: str = Path(min_length=5, max_length=20, description='Enter username',
                                            example='UrbanUser'),
                       age: int = Path(ge=18, le=120, description='Enter age', example='24')) -> str:
    try:
        edit_message = users[user_id - 1]
        edit_message.username = username
        edit_message.age = age
        return f"The user ID {user_id} is updated."
    except IndexError:
        raise HTTPException(status_code=404, detail=f"User  ID {user_id} not found")


@app.delete("/user/{user_id}")
async def delete_message(user_id: int = Path(ge=1, le=100, description='Enter User ID')) -> str:
    try:
        users.pop(user_id - 1)
        return f'User with ID {user_id} deleted'
    except IndexError:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
