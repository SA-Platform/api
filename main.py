from fastapi import FastAPI
from api.routes import divisions, announcements, users, meetings, assignments, excuses
from fastapi.middleware.cors import CORSMiddleware
app: FastAPI = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.usersRouter)
app.include_router(divisions.divisionsRouter)
app.include_router(assignments.assignmentsRouter)
app.include_router(announcements.announcementsRouter)
app.include_router(meetings.meetingsRouter)
app.include_router(excuses.excusesRouter)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True, host='localhost', port=8000)
