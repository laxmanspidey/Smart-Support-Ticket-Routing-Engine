import requests

BASE_URL = "http://127.0.0.1:8000"

test_data = [
    #{"id": "B1", "text": "I have a question about my last invoice."},
    #{"id": "L1", "text": "This is a formal legal request regarding data privacy."},
    #{"id": "U1", "text": "The server is down! Help ASAP!"}, # Should be highest priority
    {"id": "B1", "text": "I have a billing question"},
    {"id": "B2", "text": "The server is broken! Help ASAP!"},
]

def run_tests():
    print("--- Submitting Tickets ---")
    for data in test_data:
        response = requests.post(f"{BASE_URL}/tickets", json=data)
        print(f"Submitted {data['id']}: {response.json()['ticket']['category']} (Urgent: {response.json()['ticket']['is_urgent']})")

    print("\n--- Fetching from Priority Queue ---")
    # This should return 'U1' first because it's urgent
    next_ticket = requests.get(f"{BASE_URL}/tickets/next").json()
    print(f"Next up in queue: {next_ticket['ticket']['id']} - {next_ticket['ticket']['text']}")

if __name__ == "__main__":
    run_tests()