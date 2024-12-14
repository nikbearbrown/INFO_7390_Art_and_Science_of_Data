from dotenv import load_dotenv
load_dotenv()

import os

SERPAPI_PARAMS = {
    "engine": "google",
    "api_key": os.getenv("SERPAPI_KEY")
}

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")