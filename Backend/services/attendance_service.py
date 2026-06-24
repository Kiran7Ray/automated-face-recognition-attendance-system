from db import get_db_connection
from datetime import datetime

def create_attendance(data):
    conn = get_db_connection()
    cur = conn.cursor()

    date = datetime.now().date()
    day = datetime.now().strftime("%A")

    try:
        cur.execute("""
            INSERT INTO attendance (rollno, attendance_date, day, subject, status)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            data["rollno"],
            date,
            day,
            data["subject"],
            "Present"
        ))

        conn.commit()

    except Exception:
        conn.rollback()
        return {"message": "Already marked"}

    finally:
        cur.close()
        conn.close()

    return {"message": "Attendance marked"}


def get_all_attendance():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM attendance")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows