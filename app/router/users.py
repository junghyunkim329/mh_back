from fastapi import APIRouter

router = APIRouter()

# 마이페이지
@router.get("/api/{userID}")
def get_user_data(userID: int):
    return {"message": f"User {userID} data"}

# 찜 페이지
@router.get("/api/{userID}/like")
def get_user_likes(userID: int):
    return {"message": f"User {userID} likes"}

# 로드맵 모음 페이지 (확정 X)
@router.get("/api/{userID}/roadmap")
def get_user_roadmap(userID: int):
    return {"message": f"User {userID} roadmap"}

