# backend/test/tests.py
import os
import sys
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from io import BytesIO

# Add backend path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock Agent and other imports before importing anything else
sys.modules['agents'] = MagicMock()
sys.modules['agents'].Agent = MagicMock()
sys.modules['agents'].Runner = MagicMock()
sys.modules['agents'].trace = MagicMock()
sys.modules['agents'].run_crew_with_data = MagicMock(return_value="<html><body>Mock Itinerary</body></html>")
sys.modules['agents'].run_chat_with_agent = MagicMock(return_value="Mock Answer")

# Mock other dependencies
sys.modules['langchain_openai'] = MagicMock()
sys.modules['langchain_openai'].ChatOpenAI = MagicMock()

# Define mock functions for Snowflake and other services
mock_fetch_hotels = MagicMock(return_value=[{"name": "Mock Hotel"}])
mock_fetch_tours = MagicMock(return_value=[{"title": "Mock Tour"}])
mock_fetch_attractions = MagicMock(return_value=[{"title": "Mock Attraction"}])
mock_fetch_hidden_gems = MagicMock(return_value=[{"name": "Hidden Gem"}])
mock_convert_text = MagicMock(return_value="Mock Text Summary")
mock_pdf = MagicMock(return_value=BytesIO(b"%PDF-1.4\n%Mock PDF"))

# Mock location intelligence
sys.modules['location_intelligence'] = MagicMock()
sys.modules['location_intelligence'].geocode_itinerary = MagicMock(
    return_value={"all_locations": [], "locations_by_day": {}}
)
sys.modules['location_intelligence'].start_location_intelligence = MagicMock(
    return_value={"locations": [], "attractions": []}
)

# Patch external dependencies and import app
with patch('snowflake_fetch.fetch_hotels', mock_fetch_hotels), \
     patch('snowflake_fetch.fetch_tours', mock_fetch_tours), \
     patch('snowflake_fetch.fetch_attractions', mock_fetch_attractions), \
     patch('pinecone_fetch.fetch_hidden_gems', mock_fetch_hidden_gems), \
     patch('llm_formating.convert_itinerary_to_text', mock_convert_text), \
     patch('generate_pdf.create_itinerary_pdf', mock_pdf):
    
    # Import the app after all mocks are set up
    from main import app

# Create test client correctly
client = TestClient(app=app)  # Change to match the expected signature

@pytest.fixture(scope="module", autouse=True)
def set_env():
    os.environ["OPENAI_API_KEY"] = "test"
    os.environ["XAI_API_KEY"] = "test"
    os.environ["GOOGLE_MAPS_API_KEY"] = "test"
    yield

# ---------------- Valid and Working Tests ---------------- #

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "online"}

def test_generate_itinerary_valid():
    payload = {
        "city": "New York",
        "start_date": "2025-04-20",
        "end_date": "2025-04-22",
        "preference": "Suggest an itinerary with Things to do",
        "travel_type": "Solo",
        "adults": 1,
        "kids": 0,
        "budget": "medium",
        "include_tours": True,
        "include_accommodation": True,
        "include_things": True
    }
    response = client.post("/generate-itinerary", json=payload)
    assert response.status_code == 200
    data = response.json()["data"]
    assert "itinerary_html" in data
    assert "itinerary_text" in data

def test_generate_pdf_success():
    payload = {
        "city": "New York",
        "itinerary": "Mock itinerary for PDF",
        "start_date": "2025-04-20"
    }
    response = client.post("/generate-pdf", json=payload)
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"

def test_ask_question_valid():
    payload = {"itinerary": "Sample Itinerary", "question": "What places do I visit?"}
    response = client.post("/ask", json=payload)
    assert response.status_code == 200
    assert response.json() == {"answer": "Mock Answer"}