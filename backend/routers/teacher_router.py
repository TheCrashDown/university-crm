from fastapi import APIRouter


router = APIRouter()


@router.get("/watch_hometask")
def watch_hometask_endpoint():
    return {"success": True, "data": []}


@router.post("/grade_hometask")
def grade_hometask_endpoint():
    return {"success": True, "data": []}
