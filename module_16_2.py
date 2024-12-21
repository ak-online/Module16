from fastapi import FastAPI, Path
from typing import Annotated

app = FastAPI()

@app.get("/")
async def get_main_page() -> str:
    return ("Главная Страница- 16_2!")

@app.get("/user/{user_id}")
async def get_user_id(user_id: int = Path(ge=1, le=100, description="Enter user ID", example="from 1 to 100")) -> str:
    return (f"Вы вошли как пользователь N{user_id}")

@app.get("/user/{username}/{age}")
async def get_user_info(username: Annotated[str, Path(min_length=5, max_length=20, description="Enter Username", example="UrbanUser")]
               , age: int = Path(ge=18, le=120, description="Enter Age")) -> str:
    return (f"Информация о пользователе. Имя: {username}, : {age}")

