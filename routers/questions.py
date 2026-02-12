from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import services
from services.analysis_service import AnalysisServices
from services.data_service import DataServices

router = APIRouter()
templates =Jinja2Templates(directory="templates")

question_titles = {
                1: "Average tip by day",
                2: "Average total bill by time",
                3: "Tip percentage distribution",
                4: "Party size vs average tip",
                5: "Smoker vs non-smoker: average tip"}

@router.get("/", response_class=HTMLResponse)
def question_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "questions.html",
        {
            "request": request,
            "dataset_name": "tips",
            "questions": [
                {"id": 1, "title": "Average tip by day"},
                {"id": 2, "title": "Average total bill by time"},
                {"id": 3, "title": "Tip percentage distribution"},
                {"id": 4, "title": "Party size vs average tip"},
                {"id": 5, "title": "Smoker vs non-smoker: average tip"},
            ],
            "selected_question_id": None,
            "question_title": None,
            "result_html": None,
            "plot_img": None,
            "error": None
        }
    )

@router.get("/{question_id}", response_class=HTMLResponse)
def question_result(request: Request, question_id: int) -> HTMLResponse:
    data_tupl = get_data_tuple(question_id)
    # print("\n\n\n\n"+ data_tupl[2])
    return templates.TemplateResponse(
        "questions.html",
        {
            "request": request,
            "dataset_name": "tips",
            "questions": [
                {"id": 1, "title": "Average tip by day"},
                {"id": 2, "title": "Average total bill by time"},
                {"id": 3, "title": "Tip percentage distribution"},
                {"id": 4, "title": "Party size vs average tip"},
                {"id": 5, "title": "Smoker vs non-smoker: average tip"},
                ],
            "selected_question_id": question_id,
            "question_title": f"The question is: {question_titles.get(question_id, 'Unknown question')}",
            "result_html": f"{data_tupl[1].to_html()}" if data_tupl[1] is not None else "<p>No result to display.</p>",
            "plot_url": data_tupl[2], 
            "error": None
        }
    )


def get_analysis_service() -> AnalysisServices:
    return services.analysis_service

def get_data_tuple(q_id) -> str:
    return get_analysis_service().run_question(q_id)#[1].to_html()
