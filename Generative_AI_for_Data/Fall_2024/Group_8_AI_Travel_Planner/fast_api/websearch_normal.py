import requests

# Tavily API configurations
TAVILY_API_URL = "https://api.tavily.com/search"
TAVILY_API_KEY = "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"  # Replace with your API Key

def search_web(query, max_results=1):
    """
    Query Tavily API for web search results.
    """
    payload = {
        "api_key": TAVILY_API_KEY,
        "query": query,
        "max_results": max_results,
        "exclude_domains": ["youtube.com", "vimeo.com"],
        "include_raw_content": True,
    }

    response = requests.post(TAVILY_API_URL, json=payload)
    
    try:
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.json()  # Attempt to parse the response as JSON
    except requests.exceptions.HTTPError as http_err:
        return {"error": f"HTTP error occurred: {http_err} - {response.text}"}
    except requests.exceptions.RequestException as req_err:
        return {"error": f"Request error occurred: {req_err}"}
    except ValueError:
        return {"error": f"Failed to parse JSON. Response content: {response.text}"}


def generate_response(query):
    """
    Full pipeline: Search web, extract content, and format the response.
    """
    # Step 1: Search the web using Tavily
    search_results = search_web(query=query, max_results=1)
    if "error" in search_results:
        return f"Error with Tavily API: {search_results['error']}"

    # Step 2: Extract content from the first result
    if "results" in search_results and len(search_results["results"]) > 0:
        first_result = search_results["results"][0]
        url = first_result.get("url")
        title = first_result.get("title")

# Example Usage
if __name__ == "__main__":
    user_query = "5-day itinerary for Paris"
    final_response = generate_response(user_query)
    print(final_response)
