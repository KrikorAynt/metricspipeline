from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import os

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL")

conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
cursor = conn.cursor()

class Metric(BaseModel):
    user_id: str
    metric_type: str
    value: float
    timestamp: str

@app.post("/ingest/")
def ingest_metric(metric: Metric):
    try:
        cursor.execute(
            """
            SELECT 1 FROM users WHERE user_id = %s
            """,
            (metric.user_id,)
        )
        if cursor.fetchone() is None:
            raise HTTPException(status_code=404, detail="User not found.")

        cursor.execute(
            """
            SELECT session_id FROM sessions WHERE user_id = %s ORDER BY start_time DESC LIMIT 1
            """,
            (metric.user_id,)
        )
        session = cursor.fetchone()
        if not session:
            cursor.execute(
                """
                INSERT INTO sessions (user_id, start_time)
                VALUES (%s, %s) RETURNING session_id
                """,
                (metric.user_id, metric.timestamp)
            )
            session_id = cursor.fetchone()['session_id']
        else:
            session_id = session['session_id']

        cursor.execute(
            """
            INSERT INTO metrics (metric_id, session_id, timestamp, metric_type, value)
            VALUES (gen_random_uuid(), %s, %s, %s, %s)
            """,
            (session_id, metric.timestamp, metric.metric_type, metric.value)
        )
        conn.commit()
        return {"message": "Metric stored successfully!"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def read_root():
    return {"message": "Krikor's Metrics Pipeline API"}
