import os
from pinecone import Pinecone
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv(override=True)

def initialize_pinecone():
    try:
        api_key = os.getenv("PINECONE_API_KEY")
        pc = Pinecone(api_key=api_key)
        index_name = os.getenv("PINECONE_INDEX", "bigdatafinal")
        index = pc.Index(index_name)
        return index
    except Exception as e:
        print(f"Error initializing Pinecone: {e}")
        return None

def fetch_hidden_gems(city: str, limit: int = 5) -> List[Dict[Any, Any]]:
    try:
        formatted_city = format_city_name(city)
        index = initialize_pinecone()
        if not index:
            print(f"Failed to initialize Pinecone index, using fallback data")
            fallback_data = get_fallback_hidden_gems(city)
            if fallback_data:
                return fallback_data
            return []
        try:
            results = index.query(
                vector=[0] * 1536,
                filter={"city": {"$eq": formatted_city}},
                top_k=limit,
                include_metadata=True
            )
            hidden_gems = []
            for match in results.matches:
                metadata = match.metadata
                gem = {
                    "title": metadata.get("title", "Hidden Gem"),
                    "description": metadata.get("text_sample", ""),
                    "locations": metadata.get("locations", []),
                    "costs": metadata.get("costs", []),
                    "food": metadata.get("food", []),
                    "url": metadata.get("url", ""),
                    "source": metadata.get("channel", "Local Guide")
                }
                if metadata.get("time_references"):
                    gem["time_references"] = metadata.get("time_references", [])
                if metadata.get("landmarks"):
                    gem["landmarks"] = metadata.get("landmarks", [])
                if metadata.get("transport"):
                    gem["transport"] = metadata.get("transport", [])
                hidden_gems.append(gem)
            print(f"Found {len(hidden_gems)} hidden gems for {city}")
            return hidden_gems
        except Exception as query_error:
            print(f"Error querying Pinecone: {query_error}")
            fallback_data = get_fallback_hidden_gems(city)
            return fallback_data
    except Exception as e:
        print(f"Error fetching hidden gems from Pinecone: {e}")
        fallback_data = get_fallback_hidden_gems(city)
        if fallback_data:
            print(f"Using fallback data for {city}")
            return fallback_data
        return []

def format_city_name(city: str) -> str:
    city_map = {
        "New York": "NewYork",
        "San Francisco": "SanFrancisco",
        "Los Angeles": "LosAngeles",
        "Las Vegas": "LasVegas",
        "Chicago": "Chicago",
        "Seattle": "Seattle"
    }
    return city_map.get(city, city.replace(" ", ""))

def get_fallback_hidden_gems(city: str) -> List[Dict[Any, Any]]:
    fallback_data = {
        "New York": [
            {
                "title": "The High Line",
                "description": "An elevated linear park created on a former New York Central Railroad spur on the west side of Manhattan.",
                "locations": ["Chelsea", "Manhattan"],
                "costs": ["free"],
                "food": ["cafe", "food vendors"],
                "url": "https://www.thehighline.org/",
                "source": "Travel Navigator"
            },
            {
                "title": "Roosevelt Island Tramway",
                "description": "Aerial tramway that spans the East River and connects Roosevelt Island to the Upper East Side of Manhattan.",
                "locations": ["Roosevelt Island", "Manhattan"],
                "costs": ["low"],
                "food": [],
                "url": "https://rioc.ny.gov/302/Tram",
                "source": "Travel Navigator"
            },
            {
                "title": "The Cloisters",
                "description": "A branch of the Metropolitan Museum of Art dedicated to the art, architecture, and gardens of medieval Europe.",
                "locations": ["Fort Tryon Park", "Manhattan"],
                "costs": ["medium"],
                "food": ["cafe"],
                "url": "https://www.metmuseum.org/visit/plan-your-visit/met-cloisters",
                "source": "Art Explorer"
            }
        ],
        "Chicago": [
            {
                "title": "Garfield Park Conservatory",
                "description": "One of the largest and most stunning conservatories in the nation, often referred to as 'landscape art under glass'.",
                "locations": ["Garfield Park", "West Side"],
                "costs": ["free"],
                "food": ["cafe"],
                "url": "https://garfieldconservatory.org/",
                "source": "Chicago Explorer"
            },
            {
                "title": "Pilsen Murals",
                "description": "A vibrant outdoor gallery of street art in Chicago's Pilsen neighborhood, showcasing Mexican-American culture.",
                "locations": ["Pilsen", "Lower West Side"],
                "costs": ["free"],
                "food": ["mexican", "restaurant"],
                "url": "https://pilsenmuralstours.org/",
                "source": "Street Art Guide"
            },
            {
                "title": "Maxwell Street Market",
                "description": "A Chicago tradition of bargains and unique finds, plus some of the best Mexican and international street food in the city.",
                "locations": ["Near West Side", "Desplaines Street"],
                "costs": ["low"],
                "food": ["street food", "mexican", "international"],
                "url": "https://www.chicago.gov/city/en/depts/dca/supp_info/maxwell_street_market.html",
                "source": "Food Explorer"
            }
        ],
        "San Francisco": [
            {
                "title": "Sutro Baths Ruins",
                "description": "The ruins of an historic bathhouse at Lands End with stunning ocean views and hidden caves.",
                "locations": ["Lands End", "Pacific Ocean"],
                "costs": ["free"],
                "food": [],
                "landmarks": ["sutro baths", "lands end"],
                "url": "https://www.nps.gov/goga/planyourvisit/sutro-baths.htm",
                "source": "Hidden SF"
            },
            {
                "title": "16th Avenue Tiled Steps",
                "description": "A colorful 163-step mosaic stairway with incredible views of the city and ocean.",
                "locations": ["Golden Gate Heights", "Moraga Street"],
                "costs": ["free"],
                "food": [],
                "landmarks": ["16th avenue", "tiled steps"],
                "url": "https://www.16thavenuetiledsteps.com/",
                "source": "SF Explorer"
            },
            {
                "title": "Wave Organ",
                "description": "An acoustic sculpture on the bay that creates music from the waves of the ocean.",
                "locations": ["Marina District", "San Francisco Bay"],
                "costs": ["free"],
                "food": [],
                "landmarks": ["wave organ", "marina"],
                "url": "https://www.exploratorium.edu/visit/wave-organ",
                "source": "Sound Explorer"
            },
            {
                "title": "Salesforce Park",
                "description": "Elevated park built on top of the Salesforce Transit Center with gardens representing different ecosystems.",
                "locations": ["Downtown", "Transbay Terminal"],
                "costs": ["free"],
                "food": ["cafe"],
                "landmarks": ["salesforce", "transbay terminal"],
                "url": "https://salesforcetransitcenter.com/salesforce-park/",
                "source": "Urban Explorer"
            },
            {
                "title": "Angel Island",
                "description": "Historic immigration station with panoramic views of the Bay Area, accessible by ferry.",
                "locations": ["San Francisco Bay"],
                "costs": ["medium"],
                "transport": ["ferry"],
                "landmarks": ["angel island", "immigration station"],
                "url": "https://www.parks.ca.gov/?page_id=468",
                "source": "Bay Area Guide"
            }
        ],
        "Las Vegas": [
            {
                "title": "Pinball Hall of Fame",
                "description": "A museum with the world's largest pinball collection, featuring machines from the 1950s through the 1990s.",
                "locations": ["Las Vegas Strip", "East Tropicana"],
                "costs": ["low"],
                "food": [],
                "url": "http://www.pinballmuseum.org/",
                "source": "Vegas Explorer"
            },
            {
                "title": "Valley of Fire State Park",
                "description": "Nevada's oldest state park with 40,000 acres of bright red Aztec sandstone outcrops and ancient petrified trees.",
                "locations": ["Moapa Valley", "Overton"],
                "costs": ["medium"],
                "food": [],
                "url": "http://parks.nv.gov/parks/valley-of-fire",
                "source": "Nature Guide"
            },
            {
                "title": "The Neon Museum",
                "description": "An outdoor museum dedicated to preserving and exhibiting iconic Las Vegas signs.",
                "locations": ["Downtown", "Las Vegas Boulevard"],
                "costs": ["medium"],
                "food": [],
                "url": "https://www.neonmuseum.org/",
                "source": "Art Navigator"
            }
        ],
        "Los Angeles": [
            {
                "title": "The Last Bookstore",
                "description": "California's largest used and new book and record store, with quirky art installations and a labyrinth of books.",
                "locations": ["Downtown", "Spring Street"],
                "costs": ["free"],
                "food": ["cafe"],
                "url": "https://www.lastbookstorela.com/",
                "source": "LA Explorer"
            },
            {
                "title": "Venice Canals",
                "description": "A series of man-made canals built in 1905 to recreate the appearance and feel of Venice, Italy.",
                "locations": ["Venice", "Los Angeles"],
                "costs": ["free"],
                "food": [],
                "url": "https://www.laconservancy.org/locations/venice-canals",
                "source": "Hidden LA"
            },
            {
                "title": "The Museum of Jurassic Technology",
                "description": "A paradoxical museum with a bewildering array of exhibits that blur the line between fact and fiction.",
                "locations": ["Culver City", "Venice Boulevard"],
                "costs": ["low"],
                "food": [],
                "url": "https://www.mjt.org/",
                "source": "Weird LA"
            }
        ],
        "Seattle": [
            {
                "title": "Gas Works Park",
                "description": "A public park on the site of the former Seattle Gas Light Company gasification plant, with remnants of the gas works.",
                "locations": ["Lake Union", "North Seattle"],
                "costs": ["free"],
                "food": [],
                "url": "https://www.seattle.gov/parks/find/parks/gas-works-park",
                "source": "Seattle Guide"
            },
            {
                "title": "Fremont Troll",
                "description": "An 18-foot tall concrete sculpture of a troll clutching a Volkswagen Beetle, lurking under the north end of the Aurora Bridge.",
                "locations": ["Fremont", "Troll Avenue"],
                "costs": ["free"],
                "food": [],
                "url": "https://fremonttroll.com/",
                "source": "Quirky Seattle"
            },
            {
                "title": "Center for Wooden Boats",
                "description": "A maritime museum where visitors can rent boats, take sailing lessons, or join free Sunday sailing trips.",
                "locations": ["South Lake Union", "Valley Street"],
                "costs": ["free"],
                "food": [],
                "url": "https://www.cwb.org/",
                "source": "Maritime Explorer"
            }
        ]
    }
    return fallback_data.get(city, [])

if __name__ == "__main__":
    test_city = "San Francisco"
    hidden_gems = fetch_hidden_gems(test_city)
    print(f"Found {len(hidden_gems)} hidden gems for {test_city}")
    for i, gem in enumerate(hidden_gems):
        print(f"Gem {i+1}: {gem.get('title')}")
        print(f"  Description: {gem.get('description')[:100]}...")
        print(f"  Source: {gem.get('source')}")
