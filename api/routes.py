from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from models.ticket import TicketRequest, ProcessedTicket
from services.classifier import classify_ticket, check_urgency
from services.queue_manager import ticket_queue
from worker import process_ticket

router = APIRouter()

# @router.post("/tickets", response_model=dict)
# def submit_ticket(ticket: TicketRequest):
#     # Process the ticket
#     category = classify_ticket(ticket.text)
#     is_urgent = check_urgency(ticket.text)
    
#     processed_ticket = {
#         "id": ticket.id,
#         "text": ticket.text,
#         "category": category,
#         "is_urgent": is_urgent
#     }
    
#     # Store in the priority queue
#     ticket_queue.push(processed_ticket)
    
#     return {
#         "status": "success", 
#         "ticket": processed_ticket, 
#         "queue_size": ticket_queue.size()
#     }

@router.post("/tickets")
def submit_ticket(ticket: TicketRequest):
    # Dispatch task to background worker [cite: 18, 19]
    task = process_ticket.delay(ticket.id, ticket.text)
    
    # Immediately return 202 Accepted 
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content={
            "status": "Accepted for processing",
            "ticket_id": ticket.id,
            "task_id": task.id
        }
    )

@router.get("/tickets/next")
def get_next_ticket():
    """Retrieve the highest priority ticket from the queue."""
    ticket = ticket_queue.pop()
    if not ticket:
        return {"message": "Queue is empty"}
    return {"ticket": ticket}