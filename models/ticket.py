from pydantic import BaseModel

class TicketRequest(BaseModel):
    id: str
    text: str

class ProcessedTicket(BaseModel):
    id: str
    text: str
    category: str
    is_urgent: bool