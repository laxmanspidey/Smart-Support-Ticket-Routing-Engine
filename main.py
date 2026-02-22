from fastapi import FastAPI
from api.routes import router

app = FastAPI(title="Smart-Support Ticket Routing Engine - MVR")

# Include the API routes
app.include_router(router)

@app.get("/")
def health_check():
    return {"status": "MVR System is online"}