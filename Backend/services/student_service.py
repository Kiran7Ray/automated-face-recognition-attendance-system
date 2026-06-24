from db import get_db_connection

def create_student(data):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO student (rollno, fname, lname, phone, address)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        data["rollno"],
        data["fname"],
        data["lname"],
        data.get("phone"),
        data.get("address")
    ))

    conn.commit()
    cur.close()
    conn.close()

    return {"message": "Student added successfully"}


def get_all_students():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM student")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows


def delete_student(rollno):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM student WHERE rollno = %s", (rollno,))
    conn.commit()

    cur.close()
    conn.close()

    return {"message": "Student deleted"}