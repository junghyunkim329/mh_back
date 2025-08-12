from fastapi import APIRouter

router = APIRouter()

@router.get("/api/sleeping")
def get_sleeping_data():
    return {"message": "혼숙"}

@router.get("/api/sleeping/{sleepId}/review")
def get_sleeping_review(sleepId: int):
    return {"message": f"장소 {sleepId}번 혼숙 리뷰"}
