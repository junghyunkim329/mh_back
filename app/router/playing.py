from fastapi import APIRouter

router = APIRouter()

@router.get("/api/playing")
def get_playing_data():
    return {"message": "혼놀"}

@router.get("/api/playing/{playId}/review")
def get_playing_review(playId: int):
    return {"message": f"장소 {playId}번 혼놀 리뷰"}