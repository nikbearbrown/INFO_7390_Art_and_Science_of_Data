from fastapi import FastAPI, HTTPException
import os
from dotenv import load_dotenv
import requests
from typing import List, Optional
from pydantic import BaseModel

# Load environment variables
load_dotenv()
NEWS_API_KEY = os.getenv("NEWSAPI_API_KEY")

app = FastAPI()

class NewsArticle(BaseModel):
    title: str
    description: Optional[str] = None
    url: str
    urlToImage: Optional[str] = None

class NewsResponse(BaseModel):
    articles: List[NewsArticle]

@app.get("/api/f1news", response_model=NewsResponse)
async def get_f1_news():
    """Fetch Formula 1-related news articles from NewsAPI."""
    if not NEWS_API_KEY:
        raise HTTPException(status_code=500, detail="NewsAPI key not configured")
    
    url = f"https://newsapi.org/v2/everything"
    params = {
        "q": "\"Formula 1\" OR F1",
        "language": "en",
        "sortBy": "publishedAt",
        "apiKey": NEWS_API_KEY
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            articles = [
                article for article in data.get("articles", [])
                if "formula" in article["title"].lower() or "f1" in article["title"].lower()
            ][:9]  # Limit to 9 articles
            return {"articles": articles}
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"NewsAPI error: {response.json().get('message')}"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
