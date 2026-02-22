import time
import requests
from celery import Celery
import redis
from services.transformer_ml import predict_category, calculate_urgency_score

# Initialize Celery with Redis as the broker and backend 
celery_app = Celery(
    "ticket_worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

# Initialize Redis client for Atomic Locks 
redis_client = redis.Redis(host='localhost', port=6379, db=1)

WEBHOOK_URL = "https://echo.free.beeceptor.com" # Mock webhook URL for testing

@celery_app.task(bind=True)
def process_ticket(self, ticket_id: str, text: str):
    lock_key = f"lock_ticket_{ticket_id}"
    
    # Acquire Atomic Lock to prevent duplicate processing 
    # NX=True ensures the lock is only set if it doesn't exist
    lock_acquired = redis_client.set(lock_key, "locked", nx=True, ex=10)
    
    if not lock_acquired:
        return f"Ticket {ticket_id} is already being processed."

    try:
        # Run ML Models
        category = predict_category(text)
        urgency_score = calculate_urgency_score(text)
        
        print(f"[{ticket_id}] Processed: {category} | Score: {urgency_score}")

        # Integration: Trigger Webhook if S > 0.8 
        if urgency_score > 0.8:
            payload = {
                "text": f"🚨 URGENT TICKET ALERT 🚨\nID: {ticket_id}\nCategory: {category}\nScore: {urgency_score}"
            }
            requests.post(WEBHOOK_URL, json=payload)
            print(f"[{ticket_id}] Webhook fired!")

        return {"id": ticket_id, "category": category, "urgency": urgency_score}
        
    finally:
        # Release the lock once processing is done
        redis_client.delete(lock_key)