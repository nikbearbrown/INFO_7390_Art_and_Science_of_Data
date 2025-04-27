from backend.snowflake_fetch import fetch_attractions, fetch_hotels, fetch_tours, convert_decimal_to_float
from datetime import date
import json

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        return super().default(obj)

def fetch_itinerary_data(city, start_date, end_date, preference, travel_type, adults, kids, budget="medium"):
    include_tours = "Tours" in preference
    include_accommodation = "Accommodation" in preference
    include_things = "Things to do" in preference

    attractions = convert_decimal_to_float(fetch_attractions(city, budget, include_free=True)) if include_things else []
    hotels = convert_decimal_to_float(fetch_hotels(city, budget)) if include_accommodation else []
    tours = convert_decimal_to_float(fetch_tours(city, budget)) if include_tours else []

    return {
        "city": city,
        "start_date": start_date,
        "end_date": end_date,
        "travel_type": travel_type,
        "adults": adults,
        "kids": kids,
        "budget": budget,
        "attractions": attractions[:5],
        "hotels": hotels[:2],
        "tours": tours[:3]
    }
