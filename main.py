from api.routes.app import app
from fastapi.middleware.cors import CORSMiddleware

from api.routes import (
    usersRouter,
    divisionsRouter,
    rolesRouter,
    assignmentsRouter,
    announcementsRouter,
    meetingsRouter,
    submissionsRouter,
    excusesRouter,
    feedbacksRouter,
)

# set title and version for swagger
app.title = "Student Activity Platform API"
app.version = "0.0.1"

# include routers (link all of them to the main app)
app.include_router(usersRouter)
app.include_router(divisionsRouter)
app.include_router(rolesRouter)
app.include_router(assignmentsRouter)
app.include_router(announcementsRouter)
app.include_router(meetingsRouter)
app.include_router(submissionsRouter)
app.include_router(excusesRouter)
app.include_router(feedbacksRouter)

# set CORS policy
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    import sys

    # for deployment only (change localhost to 0.0.0.0)
    host = "localhost"
    reload = True
    if len(sys.argv) > 1 and sys.argv[1] == "deploy":
        host = "0.0.0.0"
        reload = False

    # run the service on the specified host and port (reload for development)
    uvicorn.run("main:app", reload=reload, host=host, port=8000)
