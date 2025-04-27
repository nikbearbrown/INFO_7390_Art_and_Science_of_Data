from crewai import Agent

from dotenv import load_dotenv

from litellm import completion

from langchain.llms.base import LLM  # Import LangChain's base LLM class

from typing import Any, List, Mapping, Optional

from datetime import datetime, timedelta

import os

import json

import math

from random import shuffle
 
load_dotenv(override=True)

#os.environ["LITELLM_API_KEY"] = os.getenv("XAI_API_KEY")
 
# Create a custom LangChain LLM wrapper for LiteLLM's Grok

class LiteLLMGrok(LLM):

    model: str = "xai/grok-2-1212"

    temperature: float = 0.7

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:

        response = completion(

            model=self.model,

            messages=[{"role": "user", "content": prompt}],

            provider="grok",

            api_key=os.getenv("XAI_API_KEY")

        )

        return response['choices'][0]['message']['content']

    @property

    def _llm_type(self) -> str:

        return "litellm-grok"

    @property

    def _identifying_params(self) -> Mapping[str, Any]:

        return {"model": self.model, "temperature": self.temperature}
 
# Create an instance of our custom LLM

custom_llm = LiteLLMGrok()
 
# Use the custom LLM in your agents

crew_agent = Agent(

    role="Travel Planner",

    goal="Generate an HTML-based multi-day travel itinerary with hidden gems",

    backstory="You are a helpful AI travel assistant who plans perfect trips based on structured data and includes insider tips about hidden gems.",

    verbose=True,

    llm=custom_llm,  # Explicitly set the LLM

)
 
chat_agent = Agent(

    role="Itinerary Q&A Expert",

    goal="Answer questions about a generated travel itinerary",

    backstory="You are a specialized AI that helps travelers understand their itinerary and answer follow-up questions based solely on the trip details provided.",

    verbose=True,

    llm=custom_llm,  # Explicitly set the LLM

)
 
def calculate_distance(lat1, lon1, lat2, lon2):

    if None in (lat1, lon1, lat2, lon2):

        return float('inf')

    try:

        lat1, lon1, lat2, lon2 = map(float, [lat1, lon1, lat2, lon2])

        R = 6371

        dLat = math.radians(lat2 - lat1)

        dLon = math.radians(lon2 - lon1)

        a = math.sin(dLat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dLon/2)**2

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

        return R * c

    except:

        return float('inf')
 
def get_coordinates(item):

    return item.get("LATITUDE"), item.get("LONGITUDE")
 
def find_closest_hotel(hotels, attractions):

    if not hotels or not attractions:

        return hotels[0] if hotels else None

    avg_lat = sum(float(a.get("LATITUDE", 0)) for a in attractions) / len(attractions)

    avg_lon = sum(float(a.get("LONGITUDE", 0)) for a in attractions) / len(attractions)

    closest_hotel = min(hotels, key=lambda h: calculate_distance(avg_lat, avg_lon, h.get("LATITUDE"), h.get("LONGITUDE")))

    return closest_hotel
 
def run_crew_with_data(data):

    try:

        start = datetime.strptime(data["start_date"], "%Y-%m-%d")

        end = datetime.strptime(data["end_date"], "%Y-%m-%d")

        num_days = (end - start).days + 1

        date_list = [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(num_days)]
 
        hotels = data.get("hotels", [])

        tours = data.get("tours", [])[:]

        attractions = data.get("attractions", [])[:]

        hidden_gems = data.get("hidden_gems", [])
 
        shuffle(tours)

        shuffle(attractions)
 
        used_tours = set()

        used_attractions = set()
 
        days = []

        for i in range(num_days):

            today_tours = []

            today_attractions = []
 
            for t in tours:

                t_id = t.get("TITLE") or t.get("URL")

                if t_id not in used_tours:

                    today_tours.append(t)

                    used_tours.add(t_id)

                if len(today_tours) == 2:

                    break
 
            for a in attractions:

                a_id = a.get("PLACENAME") or a.get("URL")

                if a_id not in used_attractions:

                    today_attractions.append(a)

                    used_attractions.add(a_id)

                if len(today_attractions) == 2:

                    break
 
            hotel = find_closest_hotel(hotels, today_attractions)
 
            days.append({

                "day": i + 1,

                "date": date_list[i],

                "hotel": hotel,

                "tours": today_tours,

                "attractions": today_attractions

            })
 
        reduced_data = {

            "city": data["city"],

            "start_date": data["start_date"],

            "end_date": data["end_date"],

            "travel_type": data["travel_type"],

            "adults": data["adults"],

            "kids": data["kids"],

            "budget": data["budget"],

            "days": days,

            "hidden_gems": hidden_gems

        }
 
        prompt = f'''

You are a travel itinerary expert.
 
Generate a professional {num_days}-day HTML travel itinerary for {data['city']} from {data['start_date']} to {data['end_date']} for {data['adults']} adults and {data['kids']} kids.
 
🎯 For each day include:

- 🏨 Hotel with NAME, ADDRESS, DISTANCE, RATING, REVIEWS, Price, CERTIFIED.

- 🚌 2 Tours with: TITLE, RATING, REVIEW COUNT, PRICE, Know More, IMAGE.

- 📍 2 Attractions with: PLACENAME, Ticket Details, HOURS, How to Reach, IMAGE, DESCRIPTION.
 
🖼️ Use this tag for all images:
<img src="{{IMAGE}}" alt="Item image" width="300" style="border-radius:10px; margin-bottom:10px;" />

Fallback if missing: https://placehold.co/400x300
 
📋 At the end, add a special section titled "Hidden Gems of {data['city']}" that showcases the local insider tips and lesser-known places. Format this section attractively with:

- A brief introduction about exploring beyond the tourist spots

- List of 3-5 hidden gems with title, description, and any relevant details like costs or food options

- Make this section visually distinct with a different background color or border
 
📦 Input JSON:

{json.dumps(reduced_data, indent=2, default=str)}
 
📋 Output rules:

- Raw HTML only (no Markdown or backticks).

- Use <div>, <h2>, <h3>, <ul>, <p>, <img>, etc.

- Use class names like "day-card", "item-section", "image-block" for structure.

- Include one section per day, clearly labeled (Day 1, Day 2, etc).

- Add a header summary at the top with trip details.

- End with the "Hidden Gems" section styled distinctly from the rest of the itinerary.

        '''
 
        response = completion(

            model="xai/grok-2-1212",

            messages=[{"role": "user", "content": prompt}],

            provider="grok",

            api_key=os.getenv("XAI_API_KEY")

        )
 
        return response['choices'][0]['message']['content']
 
    except Exception as e:

        print("Grok call error:", e)

        raise RuntimeError(f"Failed to generate itinerary from Grok: {str(e)}")
 
def run_chat_with_agent(itinerary_text: str, question: str):

    try:

        prompt = f"""You are a helpful travel assistant. Here is the travel itinerary:\n{itinerary_text}\n\nNow answer this question based on the itinerary only:\n{question}"""
 
        response = completion(

            model="xai/grok-2-1212",

            messages=[

                {"role": "system", "content": "Only answer based on the given itinerary."},

                {"role": "user", "content": prompt}

            ],

            provider="grok",

            api_key=os.getenv("XAI_API_KEY")

        )
 
        return response['choices'][0]['message']['content']

    except Exception as e:

        print("Chat Grok call error:", e)

        raise RuntimeError(f"Failed to get chat response from Grok: {str(e)}")
 
