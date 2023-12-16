from fastapi import APIRouter

from utils.util import Util

router = APIRouter()


@router.post("/upload_hometask")
def upload_hometask_endpoint():
    return {"success": True}
