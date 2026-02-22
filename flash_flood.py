import requests
import time

url = "http://127.0.0.1:8000/tickets"
# This text will be embedded and compared using Cosine Similarity
base_text = "MAJOR OUTAGE: The production database is completely down and no one can log in!"

print("🌊 Initiating Ticket Storm...")

# Sending 12 highly similar tickets to break the 10-ticket threshold
for i in range(1, 13):
    payload = {
        "id": f"STORM-{i:02d}",
        "text": base_text
    }
    response = requests.post(url, json=payload)
    print(f"Dispatched {payload['id']} - API Status: {response.status_code}")
    time.sleep(0.2) # tiny delay to simulate network traffic