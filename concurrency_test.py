import asyncio
import httpx

async def send_duplicate_ticket(client, ticket_id):
    payload = {
        "id": ticket_id,
        "text": "Simultaneous request test for atomic locking."
    }
    # Increased timeout to 30 seconds to handle the initial flood
    response = await client.post("http://127.0.0.1:8000/tickets", json=payload, timeout=30.0)
    print(f"API Response for {ticket_id}: {response.status_code}")
async def main():
    async with httpx.AsyncClient() as client:
        # Sending 15 requests for the SAME ID "STRESS-001"
        tasks = [send_duplicate_ticket(client, "STRESS-001") for _ in range(15)]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())