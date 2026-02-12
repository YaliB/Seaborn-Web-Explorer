from fastapi import APIRouter, Request
from fastapi import Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import services

router = APIRouter()
templates =Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
def data_page(
    request: Request,
    cols: list[str] | None = Query(None),
    filter_col: str | None = None,
    limit: int = 20,
    op: str | None = None,
    value: str | None = None,
) -> HTMLResponse:

    def get_data(limit: int):
        try:
            df = services.data_service.get_df()
            error_msg = None
            # --- Filtering logic ---
            if filter_col and op and value:
                try:
                    import pandas as pd
                    try:
                        val_to_use = pd.to_numeric(value)
                    except Exception:
                        val_to_use = value
                    if op == "==":
                        df = df[df[filter_col] == val_to_use]
                    elif op == "!=":
                        df = df[df[filter_col] != val_to_use]
                    elif op == ">":
                        df = df[df[filter_col] > val_to_use]
                    elif op == "<":
                        df = df[df[filter_col] < val_to_use]
                    elif op == "contains":
                        df = df[df[filter_col].astype(str).str.contains(str(value), case=False)]
                except KeyError:
                    error_msg = "The selected filter column does not exist. Please check your selection."
                except Exception:
                    error_msg = "Filtering failed. Please check the value and operator you selected."
            # ----------------------
            if cols:
                try:
                    df = df[cols]
                except KeyError:
                    error_msg = "One or more selected columns do not exist. Please check your list."
                except Exception:
                    error_msg = "Column selection failed. Please check your selection."
            table_html = df.head(limit).to_html(classes="table is-striped is-fullwidth")
            return table_html, error_msg
        except Exception:
            return None, "A general error occurred. Please try again or contact the administrator."

    # Send operators to the template to build the select element
    operators = [
        {"val": "==", "label": "=="},
        {"val": "!=", "label": "!="},
        {"val": ">", "label": ">"},
        {"val": "<", "label": "<"},
        {"val": "contains", "label": "contains"}
    ]
    
    # Send all column names (optional, so the second list is also dynamic)
    all_columns = services.data_service.get_df().columns.tolist()

    table_html, error_msg = get_data(limit=limit)
    return templates.TemplateResponse(
        "data.html",
        {
            "request": request,
            "dataset_name": "tips",
            "all_columns": all_columns, # All possible columns
            "operators": operators,     # List of operators
            "cols": cols or [],
            "filter_col": filter_col or "",
            "limit": limit,
            "op": op or "",
            "value": value or "",
            "table_html": table_html,
            "error_msg": error_msg,
        }
    )
