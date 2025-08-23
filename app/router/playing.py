from fastapi import APIRouter
import mysql.connector
import os

router = APIRouter()

def get_db():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DB")
    )

# 혼놀 가게 데이터
@router.get("/playing")
def get_playing_data():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT storeid, searchid, wide_area, basic_area, keyword, storename, category, rating, review_cnt, address, url, img_url, honbab_cnt FROM store_playing"
        )
        results = cursor.fetchall()
        cursor.close()
        db.close()
        return {"data": results}
    except Exception as e:
        return {"error": str(e)}


# 혼놀 리뷰 데이터
@router.get("/playing/{storeid}/review")
def get_eating_review(storeid: str):
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT reviewid, storeid, searchid, reviewidx, reviewtxt, url FROM review_playing WHERE storeid=%s ORDER BY reviewid",
            (storeid,)
        )
        reviews = cursor.fetchall()
        cursor.close()
        db.close()
        return {"reviews": reviews}
    except Exception as e:
        return {"error": str(e)}