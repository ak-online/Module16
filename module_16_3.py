from fastapi import FastAPI, Path, HTTPException
from typing import Annotated

app = FastAPI()
users = {'1': 'Имя: Example, возраст: 18'}


@app.get("/users")
async def get_all_users() -> dict:
    return users

@app.post("/user/{username}/{age}")
async def create_user(username: Annotated[str, Path(min_length=5, max_length=20,
                                                    description="Enter Username", example="UrbanUser")]
               , age: int = Path(ge=18, le=120, description="Enter Age")) -> str:
    user_id = str(int(max(users, key = int)) + 1)
    users[user_id] = f"Имя : {username}, возраст: {age}"
    return (f"User {user_id} is registered")

@app.put('/user/{user_id}/{username}/{age}')
async def update_users(username: Annotated[str, Path(min_length=5, max_length=20,
                                                     description='Enter username', example='UrbanUser')],
                       user_id: str = Path(min_length=1, max_length=3,
                                           description='Enter User ID', example='1'),
                       age: int = Path(ge=18, le=120, description='Enter age', example='24')) -> str:

    if user_id in users:
        users[user_id] = f"Имя : {username}, возраст: {age}"
        return f'User {user_id} has been updated.'
    else:
        return f'User with ID {user_id} not found'

@app.delete("/user/{user_id}")
async def delete_message(user_id: str = Path(min_length=1, max_length=3, description='Enter User ID', example='1'),) -> str:
    if user_id in users:
        users.pop(user_id)
        return f'User {user_id} has been updated.'
    else:
        return f'User with ID {user_id} not found'
