from fastapi import APIRouter, Body


router = APIRouter()


# --------------------- REPORT: TEXT ---------------------
@router.post("/report/unit/{unit_id}/text/", name="generate_report_unit_text", tags=["Report"])
async def report_unit_text(unit_id: int, payload: dict = Body(...)):

    return {"unit_id": unit_id, "format": "text"}


@router.post("/report/set/{set_id}/text/", name="generate_report_set_text", tags=["Report"])
async def report_set_text(set_id: int, payload: dict = Body(...)):

    return {"set_id": set_id, "format": "text"}


# --------------------- REPORT: XLSX ---------------------
@router.post("/report/unit/{unit_id}/xlsx/", name="generate_report_unit_xlsx", tags=["Report"])
async def report_unit_xlsx(unit_id: int, payload: dict = Body(...)):

    return {"unit_id": unit_id, "format": "xlsx"}


@router.post("/report/set/{set_id}/xlsx/", name="generate_report_set_xlsx", tags=["Report"])
async def report_set_xlsx(set_id: int, payload: dict = Body(...)):

    return {"set_id": set_id, "format": "xlsx"}


# --------------------- REPORT: IMAGE ---------------------
@router.post("/report/unit/{unit_id}/image/", name="generate_report_unit_image", tags=["Report"])
async def report_unit_image(unit_id: int, payload: dict = Body(...)):

    return {"unit_id": unit_id, "format": "image"}


@router.post("/report/set/{set_id}/image/", name="generate_report_set_image", tags=["Report"])
async def report_set_image(set_id: int, payload: dict = Body(...)):

    return {"set_id": set_id, "format": "image"}


# --------------------- EVALUATE: UNIT ---------------------
@router.post("/evaluate/unit/{unit_id}/break_even_point/", name="evaluate_unit_point", tags=["Evaluate"])
async def evaluate_unit_point(unit_id: int, payload: dict = Body(...)):

    return {"unit_id": unit_id, "metric": "point"}


@router.post("/evaluate/unit/{unit_id}/required_investments/", name="evaluate_unit_required", tags=["Evaluate"])
async def evaluate_unit_required(unit_id: int, payload: dict = Body(...)):

    return {"unit_id": unit_id, "metric": "required_investments"}


@router.post("/evaluate/unit/{unit_id}/expected_profit/", name="evaluate_unit_profit", tags=["Evaluate"])
async def evaluate_unit_profit(unit_id: int, payload: dict = Body(...)):

    return {"unit_id": unit_id, "metric": "expected_profit"}


# --------------------- EVALUATE: SET ---------------------
@router.post("/evaluate/set/{set_id}/break_even_point/", name="evaluate_set_point", tags=["Evaluate"])
async def evaluate_set_point(set_id: int, payload: dict = Body(...)):
    return {"set_id": set_id, "metric": "point"}


@router.post("/evaluate/set/{set_id}/required_investments/", name="evaluate_set_required", tags=["Evaluate"])
async def evaluate_set_required(set_id: int, payload: dict = Body(...)):
    return {"set_id": set_id, "metric": "required_investments"}


@router.post("/evaluate/set/{set_id}/expected_profit/", name="evaluate_set_profit", tags=["Evaluate"])
async def evaluate_set_profit(set_id: int, payload: dict = Body(...)):
    return {"set_id": set_id, "metric": "expected_profit"}


# --------------------- GET KPI: UNIT ---------------------
@router.post("/get_kpi/unit/{unit_id}/break_even_point/", name="get_kpi_unit_point", tags=["Get KPI"])
async def get_kpi_unit_point(unit_id: int, payload: dict = Body(...)):
    return {"unit_id": unit_id, "metric": "point"}


@router.post("/get_kpi/unit/{unit_id}/required_investments/", name="get_kpi_unit_required", tags=["Get KPI"])
async def get_kpi_unit_required(unit_id: int, payload: dict = Body(...)):
    return {"unit_id": unit_id, "metric": "required_investments"}


@router.post("/get_kpi/unit/{unit_id}/expected_profit/", name="get_kpi_unit_profit", tags=["Get KPI"])
async def get_kpi_unit_profit(unit_id: int, payload: dict = Body(...)):
    return {"unit_id": unit_id, "metric": "expected_profit"}