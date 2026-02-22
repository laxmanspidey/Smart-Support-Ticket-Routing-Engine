import asyncio
import httpx
import time
import requests

BASE_URL = "http://127.0.0.1:8000/tickets"

def test_standard_routing():
    print("\n--- TEST 1: Standard Routing & Low Urgency (Milestone 2 & 3) ---")
    payload = {"id": "TEST-001", "text": "Can I get a copy of my recent invoice?"}
    response = requests.post(BASE_URL, json=payload)
    print(f"API Status: {response.status_code} (Expected: 202)")
    print("Action: Check worker logs for 'Billing', low score S < 0.8, and routing to an agent.")
    time.sleep(3) # Wait for worker to process

def test_urgent_webhook():
    print("\n--- TEST 2: High Urgency & Webhook Trigger (Milestone 2) ---")
    payload = {"id": "TEST-002", "text": "This is terrible! The system crashed and I am losing money! Fix ASAP!"}
    response = requests.post(BASE_URL, json=payload)
    print(f"API Status: {response.status_code} (Expected: 202)")
    print("Action: Check worker logs for score S > 0.8 and 'Webhook fired!'.")
    time.sleep(3)

async def test_atomic_locks():
    print("\n--- TEST 3: Concurrency & Atomic Locks (Milestone 2) ---")
    print("Sending 5 simultaneous requests with the EXACT SAME ID...")
    
    async def send_duplicate(client, i):
        payload = {"id": "LOCK-TEST-99", "text": "Testing atomic locks."}
        # Added timeout=30.0 here to prevent the ReadTimeout!
        resp = await client.post(BASE_URL, json=payload, timeout=30.0)
        return resp.status_code

    async with httpx.AsyncClient() as client:
        tasks = [send_duplicate(client, i) for i in range(5)]
        await asyncio.gather(*tasks)
        
    print("Action: Check worker logs. It should process LOCK-TEST-99 EXACTLY ONCE. The others should say 'Duplicate processing prevented'.")
    time.sleep(3)

def test_flash_flood():
    print("\n--- TEST 4: Semantic Deduplication / Ticket Storm (Milestone 3) ---")
    print("Sending 11 highly similar tickets to trigger the Master Incident...")
    base_text = "The entire database cluster is down and returning 500 errors."
    
    for i in range(1, 12):
        payload = {"id": f"STORM-TEST-{i:02d}", "text": base_text}
        requests.post(BASE_URL, json=payload)
    
    print("Action: Check worker logs. Tickets 1-10 should route normally. Ticket 11 should trigger '🚨 TICKET STORM DETECTED! Master Incident created'.")

if __name__ == "__main__":
    test_standard_routing()
    test_urgent_webhook()
    asyncio.run(test_atomic_locks())
    test_flash_flood()