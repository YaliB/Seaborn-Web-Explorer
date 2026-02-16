from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routers.pages import router as pages_router
from routers.questions import router as questions_router
from routers.data import router as data_router


templates =Jinja2Templates(directory="templates")
app = FastAPI(title="Tips Manager")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(pages_router)
app.include_router(questions_router, prefix="/questions", tags=["Questions"])
app.include_router(data_router, prefix="/data", tags=["Data"])

print("The server was loaded successfully")


@app.exception_handler(404)
async def custom_404_handler(request: Request, exc):
    return templates.TemplateResponse(
        "404.html", {"request": request}, status_code=404
    )