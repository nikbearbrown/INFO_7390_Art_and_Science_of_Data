import requests

# Tavily API Base URL
TAVILY_API_URL = "https://api.tavily.com/search"
TAVILY_API_KEY = "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"  # Replace with your API Key

def search_youtube(query, max_results=1):
    """
    Function to query the Tavily API for YouTube video search.
    
    Args:
        query (str): The search query.
        max_results (int): Maximum number of YouTube results to return (default is 1).
    
    Returns:
        dict: Response data from the Tavily API or an error message.
    """
    payload = {
        "api_key": TAVILY_API_KEY,
        "query": query,
        "max_results": max_results,
        "include_domains": ["youtube.com"],  # Restrict to video platforms
        "include_images": False,
    }

    try:
        response = requests.post(TAVILY_API_URL, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Error: {response.status_code} - {response.json().get('message', 'Unknown error')}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {e}"}
