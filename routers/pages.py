from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates =Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
def home(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "dataset_name": "tips"
        }
    )


async def custom_404_handler(request, exc):
    return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
