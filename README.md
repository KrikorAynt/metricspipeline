# Metrics Ingestion Pipeline
## Overview
This repository contains a metrics ingestion pipeline designed to collect and store user metrics, such as talked_time, microphone_used, speaker_used, and voice_sentiment. The solution is built using FastAPI and PostgreSQL, with each service running in a separate Docker container.

## Prerequisites
* Docker Desktop installed on your Windows machine.
* Basic understanding of Docker, Docker Compose, and PostgreSQL.

## Setup Instructions
1. Launch Docker Desktop
2. Optional: You can change the environment variables for the database by changing the 'docker-compose.yml' file
3. Navigate to the local repo in your cmd, then run the command:
   ```
   docker-compose up --build
   ```
   You may have to start the metrics_app container in Docker Desktop on the first run.

   
4. To interact with the API, you can use "curl". Example usage:
   ```
   curl -X POST "http://localhost:8000/ingest/" -H "Content-Type: application/json" -d ^
    "{\"user_id\":\"b2a7465b-5d83-40c6-b8b6-2f8f15cbf23d\",\"metric_type\":\"talked_time\",\"value\":12.34,\"timestamp\":\"2024-08-08T12:34:56Z\"}"
   ```
   You will have to create a user to attach the metrics. An example for how this would look:
   ```
   docker exec -it metrics_db psql -U metrics_user -d metrics_db
   ```
   Then in the following psql terminal:
   ```
   INSERT INTO public.users (user_id, name, email)
   VALUES ('b2a7465b-5d83-40c6-b8b6-2f8f15cbf23d', 'Greg', 'greg@gmail.com');
   ```
   If everything is set up correctly you should see:
    ```
    {"message":"Metric stored successfully!"}
    ```

Database Schema
The database schema consists of the following tables:
```
users
  user_id (UUID, Primary Key)
  name (VARCHAR)
  email (VARCHAR)

sessions
  session_id (UUID, Primary Key)
  user_id (UUID, Foreign Key referencing users.user_id)
  start_time (TIMESTAMP)

metrics
  metric_id (UUID, Primary Key)
  session_id (UUID, Foreign Key referencing sessions.session_id)
  timestamp (TIMESTAMP)
  metric_type (VARCHAR)
  value (FLOAT)
```

## Adding New Metrics
To add new metrics:
1. Update the metrics table to include additional columns or adjust the existing ones.
2. Modify the FastAPI application to handle the new metric type.
## Scaling the Pipeline
Consider partitioning the metrics table by time or user to improve query performance.

## Future Improvements
- Add support for batch metric ingestion to improve efficiency.
- Add commenting for code readablity
  
