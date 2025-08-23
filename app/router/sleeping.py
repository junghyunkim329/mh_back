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

@router.get("/sleeping")
def get_sleeping_data():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT storeid, searchid, wide_area, basic_area, keyword, storename, category, rating, review_cnt, address, url, img_url, honbab_cnt FROM store_sleeping"
        )
        results = cursor.fetchall()
        cursor.close()
        db.close()
        return {"data": results}
    except Exception as e:
        return {"error": str(e)}


@router.get("/sleeping/{storeid}/review")
def get_sleeping_review(storeid: str):
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT reviewid, storeid, searchid, reviewidx, reviewtxt, url FROM review_sleeping WHERE storeid=%s ORDER BY reviewid",
            (storeid,)
        )
        reviews = cursor.fetchall()
        cursor.close()
        db.close()
        return {"reviews": reviews}
    except Exception as e:
        return {"error": str(e)}