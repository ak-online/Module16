from fastapi import FastAPI, Path, status, Body, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from typing import Annotated, List
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory='templates')

users = []

class User(BaseModel):
    id: int = None
    username: str
    age: int

@app.get('/')
def get_all_users(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('users.html',{'request': request, 'users': users})

@app.get('/user/{user_id}')
def get_user(request: Request, user_id: int) -> HTMLResponse:
    try:
        return templates.TemplateResponse('users.html', {'request':request, 'user': users[user_id-1]})
    except IndexError:
        raise HTTPException(status_code=404, detail="Message not found")

@app.post('/user/{username}/{age}')
def create_user(username: Annotated[str, Path(min_length=4, max_length=20, description='Enter username')],
                    age: Annotated[int, Path(ge=18, le=120, description='Enter age')]) -> User:


    # if len(users) != 0:
    #     new_id = len(users) + 1
    # else:
    #     new_id = 1
    new_id = len(users)+1
    new_user = User(id=new_id, username=username, age=age)
    users.append(new_user)
    return new_user

@app.put('/user/{user_id}/{username}/{age}')
async def update_users(user_id: int = Path(ge=1, le=100, description='Enter User ID'),
                       username: str = Path(min_length=5, max_length=20, description='Enter username',
                                            example='UrbanUser'),
                       age: int = Path(ge=18, le=120, description='Enter age', example='24')) -> str:
# def update_user(user_id: Annotated[int, Path(ge=1, le=100, description='Enter User ID')],
#                       username: Annotated[str, Path(min_length=4, max_length=20, description='Enter username')],
#                       age: Annotated[int, Path(ge=18, le=120, description='Enter age')]) -> User:
    # for user in users:
    #     if user.id == user_id:
    #         user.username = username
    #         user.age = age
    #         return user
    # else:
    #     raise HTTPException(status_code=404, detail='Пользователя не существует')
    try:
        edit_message = users[user_id - 1]
        edit_message.username = username
        edit_message.age = age
        return f"The user ID {user_id} is updated."
    except IndexError:
        raise HTTPException(status_code=404, detail=f"User  ID {user_id} not found")


@app.delete('/user/{user_id}')
async def delete_user(user_id: int = Path(ge=1, le=100, description='Enter User ID')) -> str:
    try:
        users.pop(user_id - 1)
        return f'User with ID {user_id} deleted'
    except IndexError:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
# def delete_user(user_id: int) -> str:
#     for i, user in enumerate(users):
#         if user.id == user_id:
#             return users.pop(i)
#     else:
#         raise HTTPException(status_code=404, detail='Пользователя не существует')