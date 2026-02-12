from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers.pages import router as pages_router
from routers.questions import router as questions_router
from routers.data import router as data_router

app = FastAPI(title="Tips Manager")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(pages_router)
app.include_router(questions_router, prefix="/questions", tags=["Questions"])
app.include_router(data_router, prefix="/data", tags=["Data"])

print("The server was loaded successfully")