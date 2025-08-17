from fastapi import APIRouter, Request, Form, HTTPException
from passlib.context import CryptContext
import mysql.connector
import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# DB 연결 함수
def get_db():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DB")
    )

router = APIRouter()

# 요청 Body 스키마 정의
class SignupRequest(BaseModel):
    UserName: str
    UserID: str
    UserPW: str

class LoginRequest(BaseModel):
    UserID: str
    UserPW: str

# 회원가입
@router.post("/api/signup")
async def signup(user: SignupRequest):
    if not user.UserName or not user.UserID or not user.UserPW:
        raise HTTPException(status_code=400, detail="모든 필드를 입력하세요.")

    hashed_pw = pwd_context.hash(user.UserPW)
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO user (UserName, UserID, UserPW) VALUES (%s, %s, %s)",
            (user.UserName, user.UserID, hashed_pw)
        )
        conn.commit()
    except mysql.connector.Error as err:
        if err.errno == 1062:  # 중복 키 에러
            raise HTTPException(status_code=400, detail="이미 존재하는 아이디입니다.")
        else:
            raise HTTPException(status_code=500, detail=f"DB 오류: {err}")
    finally:
        cursor.close()
        conn.close()
    return {"message": "회원가입 성공!"}

# 로그인
@router.post("/api/login")
async def login(user: LoginRequest, request: Request):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user WHERE UserID = %s", (user.UserID,))
    user_db = cursor.fetchone()
    cursor.close()
    conn.close()

    if not user_db:
        raise HTTPException(status_code=401, detail="존재하지 않는 아이디입니다.")
    if not pwd_context.verify(user.UserPW, user_db["UserPW"]):
        raise HTTPException(status_code=401, detail="비밀번호가 일치하지 않습니다.")

    request.session["user"] = {"id": user_db["UserID"], "name": user_db["UserName"]}
    return{
     "message": "로그인 성공!",
     "UserName": user_db["UserName"]
    }

# 로그아웃
@router.post("/api/logout")
async def logout(request: Request):
    request.session.clear()
    return {"message": "로그아웃 되었습니다."}

# '''
# from fastapi import APIRouter

# router = APIRouter()
# '''
# from fastapi import APIRouter, Request, Form, HTTPException
# from passlib.context import CryptContext
# import mysql.connector
# import os
# from dotenv import load_dotenv

# load_dotenv()

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# def get_db():
#     return mysql.connector.connect(
#         host=os.getenv("MYSQL_HOST"),
#         user=os.getenv("MYSQL_USER"),
#         password=os.getenv("MYSQL_PASSWORD"),
#         database=os.getenv("MYSQL_DB")
#     )

# router = APIRouter()

# @router.post("/api/signup")
# async def signup(id: str = Form(...), pw: str = Form(...), name: str = Form(...)):
#     if not id or not pw or not name:
#         raise HTTPException(status_code=400, detail="모든 필드를 입력하세요.")
#     hashed_pw = pwd_context.hash(pw)
#     conn = get_db()
#     cursor = conn.cursor()
#     try:
#         cursor.execute(
#             "INSERT INTO user (UserID, UserPW, UserName) VALUES (%s, %s, %s)",
#             (id, hashed_pw, name)
#         )
#         conn.commit()
#     except mysql.connector.Error as err:
#         if err.errno == 1062:
#             raise HTTPException(status_code=400, detail="이미 존재하는 아이디입니다.")
#         else:
#             raise HTTPException(status_code=500, detail="DB 오류")
#     finally:
#         cursor.close()
#         conn.close()
#     return {"message": "회원가입 성공!"}

# @router.post("/api/login")
# async def login(request: Request, id: str = Form(...), pw: str = Form(...)):
#     conn = get_db()
#     cursor = conn.cursor(dictionary=True)
#     cursor.execute("SELECT * FROM user WHERE UserID = %s", (id,))
#     user = cursor.fetchone()
#     cursor.close()
#     conn.close()

#     if not user:
#         raise HTTPException(status_code=401, detail="존재하지 않는 아이디입니다.")
#     if not pwd_context.verify(pw, user["UserPW"]):
#         raise HTTPException(status_code=401, detail="비밀번호가 일치하지 않습니다.")

#     request.session["user"] = {"id": user["UserID"], "name": user["UserName"]}
#     return {"message": "로그인 성공!"}

# @router.get("/api/me")
# async def me(request: Request):
#     user = request.session.get("user")
#     if user:
#         return user
#     raise HTTPException(status_code=401, detail="로그인 필요")

# @router.post("/api/logout")
# async def logout(request: Request):
#     request.session.clear()
#     return {"message": "로그아웃 되었습니다."}

# '''
# @router.post("/api/new-user/")
# def signup(user: dict):
#     # 회원가입 처리
#     return {"message": "회원가입 완료"}

# @router.post("/api/user/")
# def login(user: dict):
#     # 로그인 처리
#     return {"message": "로그인 성공"}

# @router.post("/api/logout/")
# def logout():
#     # 로그아웃 처리
#     return {"message": "로그아웃 완료"}
#     '''