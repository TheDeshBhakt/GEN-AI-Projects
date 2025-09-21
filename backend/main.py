import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import your custom modules
from scraper import scrape_sites
from rag_pipeline import get_answer_from_query


app = FastAPI(
    title="Varanasi AI Guide API",
    description="API for the Varanasi AI Guide, providing information and stories about the city.",
    version="1.0.0",
)

# --- CORS Middleware ---
# This is crucial for allowing the frontend to communicate with the backend
origins = [
    "http://localhost:3000",  # Default for many frontend dev servers
    "http://localhost:5173",  # Default for Vite/Svelte
    # Add the production frontend URL here when you have it
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic Models ---
class ChatQuery(BaseModel):
    query: str

# --- API Endpoints ---
@app.get("/", tags=["Health Check"])
def read_root():
    """A simple endpoint to check if the API is running."""
    return {"status": "ok", "message": "Welcome to the Varanasi AI Guide API!"}

@app.post("/api/scrape", tags=["Scraping"])
def trigger_scraping():
    """Triggers the web scraping process to update the data."""
    try:
        result = scrape_sites()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat", tags=["AI Chat"])
def chat_with_agent(chat_query: ChatQuery):
    """
    The main endpoint for the user to interact with the AI agent.
    Takes a user query and returns a generated answer.
    """
    if not chat_query.query:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
    try:
        answer = get_answer_from_query(chat_query.query)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- To run this application ---
# In your terminal, from the 'backend' directory:
# uvicorn main:app --reload
#
# The API will be available at http://127.0.0.1:8000
# You can see the interactive API documentation at http://127.0.0.1:8000/docs
