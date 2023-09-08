from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import divisions, announcements, users, meetings, assignments, excuses, feedback, submissions, roles

app: FastAPI = FastAPI(
    title="Student Activity Platform API",
    version="0.0.1",
)

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
app.include_router(roles.rolesRouter)
app.include_router(assignments.assignmentsRouter)
app.include_router(announcements.announcementsRouter)
app.include_router(meetings.meetingsRouter)
app.include_router(submissions.submissionsRouter)
app.include_router(excuses.excusesRouter)
app.include_router(feedback.feedbacksRouter)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True, host='localhost', port=8000)
