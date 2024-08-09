curl -X POST "http://localhost:8000/ingest/" -H "Content-Type: application/json" -d \
'{
    "user_id": "user-1234",
    "session_id": "session-5678",
    "metric_type": "talked_time",
    "value": 12.34,
    "timestamp": "2024-08-08T12:34:56Z"
}'
