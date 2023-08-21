from fastapi import FastAPI, status
from api.routers import divisions, announcements, users

app: FastAPI = FastAPI()
app.include_router(users.usersRouter)
app.include_router(divisions.divisionsRouter)
app.include_router(announcements.announcementsRouter)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)