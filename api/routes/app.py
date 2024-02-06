from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app: FastAPI = FastAPI()


@app.get("/", include_in_schema=False)
async def redirect_docs():
    return RedirectResponse(url="/docs")