import os
import traceback
import logging
import uvicorn
from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator
from datetime import date
from typing import Literal
from dotenv import load_dotenv
from agents import run_crew_with_data, run_chat_with_agent
from snowflake_fetch import (
    fetch_attractions,
    fetch_hotels,
    fetch_tours,
    convert_decimal_to_float
)
from pinecone_fetch import fetch_hidden_gems
from llm_formating import convert_itinerary_to_text
from generate_pdf import create_itinerary_pdf

load_dotenv(override=True)
os.environ["LITELLM_API_KEY"] = os.getenv("XAI_API_KEY")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class ItineraryInput(BaseModel):
    city: str
    start_date: date
    end_date: date
    preference: Literal[
        "Suggest an itinerary with Tours, Accommodation, Things to do",
        "Suggest an itinerary with Accommodation, Things to do",
        "Suggest an itinerary with Things to do"
    ]
    travel_type: Literal["Solo", "With Family"]
    adults: int = 1
    kids: int = 0
    budget: Literal["low", "medium", "high"] = "medium"
    include_tours: bool = True
    include_accommodation: bool = True
    include_things: bool = True

    @field_validator('end_date')
    def end_date_after_start(cls, end_date, values):
        if 'start_date' in values.data and end_date < values.data['start_date']:
            raise ValueError("End date must be after start date")
        return end_date

class ChatRequest(BaseModel):
    itinerary: str
    question: str

class PDFRequest(BaseModel):
    city: str
    itinerary: str
    start_date: str

class RawDataRequest(BaseModel):
    city: str
    budget: Literal["low", "medium", "high"] = "medium"
    include_accommodation: bool = True
    include_tours: bool = True
    include_things: bool = True

def fetch_itinerary_data(city, start_date, end_date, travel_type, adults, kids, budget,
                         include_tours=True, include_accommodation=True, include_things=True):
    logger.info("FETCHING ITINERARY DATA")
    logger.info(f"City: {city}, Budget: {budget}, Start: {start_date}, End: {end_date}")
    logger.info(f"Include Tours: {include_tours}, Include Accommodations: {include_accommodation}, Include Things to Do: {include_things}")
    hotels = convert_decimal_to_float(fetch_hotels(city, budget)) if include_accommodation else []
    logger.info(f"Fetched {len(hotels)} hotels")
    tours = convert_decimal_to_float(fetch_tours(city, budget)) if include_tours else []
    logger.info(f"Fetched {len(tours)} tours")
    attractions = convert_decimal_to_float(fetch_attractions(city, budget, include_free=True)) if include_things else []
    logger.info(f"Fetched {len(attractions)} attractions")
    hidden_gems = fetch_hidden_gems(city)
    logger.info(f"Fetched {len(hidden_gems)} hidden gems")

    return {
        "city": city,
        "start_date": str(start_date),
        "end_date": str(end_date),
        "travel_type": travel_type,
        "adults": adults,
        "kids": kids,
        "budget": budget,
        "hotels": hotels,
        "tours": tours,
        "attractions": attractions,
        "hidden_gems": hidden_gems
    }

@app.get("/")
def root():
    logger.info("Health check endpoint called")
    return {"status": "online"}

@app.post("/generate-itinerary")
def generate_itinerary(payload: ItineraryInput):
    try:
        logger.info("Generating itinerary")
        structured_data = fetch_itinerary_data(
            city=payload.city,
            start_date=payload.start_date,
            end_date=payload.end_date,
            travel_type=payload.travel_type,
            adults=payload.adults,
            kids=payload.kids,
            budget=payload.budget,
            include_tours=payload.include_tours,
            include_accommodation=payload.include_accommodation,
            include_things=payload.include_things
        )

        html = run_crew_with_data(structured_data)
        text_summary = convert_itinerary_to_text(html)

        logger.info("Itinerary generation successful")
        return {
            "status": "success",
            "data": {
                "itinerary_html": html,
                "itinerary_text": text_summary
            }
        }

    except Exception as e:
        logger.error("Error generating itinerary", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error generating itinerary: {str(e)}")

@app.post("/generate-pdf")
def generate_pdf(payload: PDFRequest):
    try:
        logger.info(f"Generating PDF for city: {payload.city}")
        pdf_bytes = create_itinerary_pdf(payload.city, payload.itinerary, payload.start_date)

        if not pdf_bytes or pdf_bytes.getbuffer().nbytes == 0:
            raise ValueError("Generated PDF is empty.")

        logger.info("PDF generation successful")
        return Response(
            content=pdf_bytes.getvalue(),
            media_type="application/pdf"
        )

    except Exception as e:
        logger.error("Error generating PDF", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error generating PDF: {str(e)}")

@app.post("/ask")
def ask_question(req: ChatRequest):
    try:
        logger.info("Handling chat request")
        answer = run_chat_with_agent(req.itinerary, req.question)
        return {"answer": answer}
    except Exception as e:
        logger.error("Error during chat handling", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    logger.info(f"Starting server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)