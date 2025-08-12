from fastapi import APIRouter

router = APIRouter()

@router.get("/api/eating")
def get_eating_data():
    return {"message": "혼밥"}

@router.get("/api/eating/{eatId}/review")
def get_eating_review(eatId: int):
    return {"message": f"가게 {eatId}번 혼밥 리뷰"}