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

@router.get("/api/sleeping")
def get_sleeping_data():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT 
                storeid AS storeId,
                searchid AS searchId,
                wide_area,
                basic_area,
                keyword,
                storename AS name,
                category,
                rating,
                review_cnt,
                address,
                url,
                img_url AS main_photo
            FROM store_sleeping
            """
        )
        results = cursor.fetchall()
        cursor.close()
        db.close()
        return {"data": results}
    except Exception as e:
        return {"error": str(e)}


@router.get("/api/sleeping/{storeid}/review")
def get_sleeping_review(storeid: str):
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT 
                reviewid AS reviewId,
                storeid AS storeId,
                searchid AS searchId,
                reviewidx AS reviewIdx,
                reviewtxt AS reviewTxt
            FROM review_sleeping
            WHERE storeid=%s
            ORDER BY reviewid
            """,
            (storeid,)
        )
        reviews = cursor.fetchall()
        cursor.close()
        db.close()
        return {"reviews": reviews}
    except Exception as e:
        return {"error": str(e)}