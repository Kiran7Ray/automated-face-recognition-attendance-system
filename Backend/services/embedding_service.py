from db import get_db_connection

def store_embedding(data):
    conn = get_db_connection()
    cur = conn.cursor()

    embedding = data["embedding"]  # list of 128 floats

    cur.execute("""
        INSERT INTO embeddings (rollno, embedding)
        VALUES (%s, %s)
        ON CONFLICT (rollno)
        DO UPDATE SET embedding = EXCLUDED.embedding
    """, (data["rollno"], embedding))

    conn.commit()
    cur.close()
    conn.close()

    return {"message": "Embedding stored"}