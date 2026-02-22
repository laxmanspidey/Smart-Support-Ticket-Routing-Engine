from fastapi import FastAPI
from api.routes import router
import redis

app = FastAPI(title="Smart-Support Ticket Routing Engine - MVR")

# Include the API routes
app.include_router(router)
redis_client = redis.Redis(host='localhost', port=6379, db=1)

@app.get("/")
def health_check():
    return {"status": "MVR System is online"}

@app.get("/logs")
def get_recent_logs():
    """Fetches the latest logs from the Celery workers"""
    # Fetch the 20 most recent logs
    raw_logs = redis_client.lrange("system_logs", 0, 19)
    # Decode from bytes to strings
    logs = [log.decode('utf-8') for log in raw_logs]
    return {"logs": logs}