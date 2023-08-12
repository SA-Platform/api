from typing import Union

from fastapi import FastAPI, status

from api.validators import UserValidator

app = FastAPI()

@app.post("/signup", tags=["Users"], status_code= status.HTTP_201_CREATED)
async def signup(request: UserValidator):
    return {"text": "write"}
