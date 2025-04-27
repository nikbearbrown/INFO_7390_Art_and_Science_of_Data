import os
import snowflake.connector
import pandas as pd
from dotenv import load_dotenv
import math
import re
from decimal import Decimal

load_dotenv(override=True)

def convert_decimal_to_float(obj):
    """Convert Decimal values to float for JSON serialization"""
    if isinstance(obj, dict):
        return {k: convert_decimal_to_float(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_decimal_to_float(item) for item in obj]
    elif isinstance(obj, Decimal):
        return float(obj)
    else:
        return obj

def get_connection():
    """Establish connection to Snowflake"""
    try:
        return snowflake.connector.connect(
            user=os.getenv("SNOWFLAKE_USER"),
            password=os.getenv("SNOWFLAKE_PASSWORD"),
            account=os.getenv("SNOWFLAKE_ACCOUNT"),
            warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
            database=os.getenv("SNOWFLAKE_DATABASE"),
            schema=os.getenv("SNOWFLAKE_SCHEMA"),
            role=os.getenv("SNOWFLAKE_ROLE")
        )
    except Exception as e:
        print(f"Error connecting to Snowflake: {e}")
        raise

def fetch_attractions(city, budget="medium", include_free=True):
    """
    Fetch attractions data for a specific city with error handling and budget filtering
    
    Args:
        city: City name to search for
        budget: 'low', 'medium', or 'high'
        include_free: Whether to include free attractions
    """
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        standardized_city = standardize_city_name(city)
        query = f"""
        SELECT * FROM ATTRACTION 
        WHERE (CITY ILIKE '%{standardized_city}%' 
        OR CITY ILIKE '%{standardized_city} United States%')
        """
        
        print(f"Executing attractions query for city: {standardized_city}")
        cursor.execute(query)
        
        columns = [desc[0] for desc in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        results = convert_decimal_to_float(results)
        
        # Process the results to determine if attractions are free and their price range
        processed_results = []
        
        for attraction in results:
            is_free = is_attraction_free(attraction)
            
            price_value = 0
            if not is_free:
                price_value = extract_price_from_ticket_details(attraction.get('Ticket Details', ''))
            
            # Add flags to the attraction
            attraction['IsFree'] = is_free
            attraction['PriceValue'] = price_value
            
            # Determine which budget category this fits
            if is_free:
                # Always include free attractions if requested
                if include_free:
                    processed_results.append(attraction)
            else:
                # For paid attractions, filter by budget
                if budget == "low" and price_value <= 50:
                    processed_results.append(attraction)
                elif budget == "medium" and price_value <= 150:
                    processed_results.append(attraction)
                elif budget == "high" or price_value > 150:
                    processed_results.append(attraction)
        
        sorted_results = sorted(processed_results, 
                              key=lambda x: float(x.get('RATING', 0) or 0), 
                              reverse=True)
        
        print(f"Fetched {len(sorted_results)} attractions for {standardized_city} with budget {budget}")
        return sorted_results
    
    except Exception as e:
        print(f"Error fetching attractions: {e}")
        return []
    
    finally:
        if conn:
            conn.close()

def fetch_hotels(city, budget="medium", top_n=5):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        standardized_city = standardize_city_name(city)
        
        query = f"""
        SELECT * FROM HOTEL_DATA 
        WHERE CITY ILIKE '%{standardized_city}%'
        """
        
        print(f"Executing hotels query for city: {standardized_city}")
        cursor.execute(query)
        
        columns = [desc[0] for desc in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        # Convert Decimal values to float for JSON serialization
        results = convert_decimal_to_float(results)
        
        # Process hotels to extract price values and filter out those with no price
        hotels_with_price = []
        
        for hotel in results:
            # Get price using the exact column name "Price (per night)"
            price_text = hotel.get('Price (per night)', '')
            
            # Skip hotels with no price or empty price string
            if not price_text or price_text.strip() == '':
                print(f"Skipping hotel with no price: {hotel.get('NAME', 'Unknown')}")
                continue
                
            # Extract price value
            price_value = extract_price(price_text)
            
            # Skip hotels where price extraction failed (returned 0 or negative)
            if price_value <= 0:
                print(f"Skipping hotel with invalid price: {hotel.get('NAME', 'Unknown')} ('{price_text}')")
                continue
                
            # Add price value to hotel data
            hotel['PriceValue'] = price_value
            
            # Convert rating to numeric if it's not already
            if hotel.get('RATING') and not isinstance(hotel.get('RATING'), (int, float)):
                try:
                    hotel['RATING'] = float(hotel['RATING'])
                except ValueError:
                    hotel['RATING'] = 0
            
            # Add to list of hotels with valid prices
            hotels_with_price.append(hotel)
        
        print(f"Found {len(hotels_with_price)} hotels with valid prices out of {len(results)} total")
        
        # If we have no hotels with valid prices, return empty list
        if not hotels_with_price:
            return []
        
        # Define price thresholds for different budgets
        if budget == "low":
            filtered_hotels = [h for h in hotels_with_price if h.get('PriceValue', 0) <= 150]
        elif budget == "medium":
            filtered_hotels = [h for h in hotels_with_price if 150 < h.get('PriceValue', 0) <= 350]
        else:  # high budget
            filtered_hotels = [h for h in hotels_with_price if h.get('PriceValue', 0) > 350]
        
        # If we don't have enough hotels in the specific budget range, include others
        if len(filtered_hotels) < top_n:
            # Sort all hotels by price
            all_sorted = sorted(hotels_with_price, key=lambda x: x.get('PriceValue', 0))
            
            # For low budget, add the cheapest available
            if budget == "low":
                filtered_hotels = all_sorted[:min(top_n, len(all_sorted))]
            # For high budget, add the most expensive
            elif budget == "high":
                filtered_hotels = all_sorted[-min(top_n, len(all_sorted)):]
            # For medium budget, add a mix
            else:
                mid_point = len(all_sorted) // 2
                start_idx = max(0, mid_point - top_n // 2)
                end_idx = min(len(all_sorted), start_idx + top_n)
                filtered_hotels = all_sorted[start_idx:end_idx]
        
        # Sort by a combination of rating and price appropriateness for the budget
        sorted_results = sort_hotels_by_value(filtered_hotels, budget)
        
        # Return the top N hotels (or fewer if not enough available)
        top_hotels = sorted_results[:min(top_n, len(sorted_results))]
        
        print(f"Returning {len(top_hotels)} hotels for {standardized_city} with budget {budget}")
        return top_hotels
    
    except Exception as e:
        print(f"Error fetching hotels: {e}")
        return []
    
    finally:
        if conn:
            conn.close()

def fetch_tours(city, budget="medium"):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Standardize city name for query
        standardized_city = standardize_city_name(city)
        
        query = f"""
        SELECT * FROM TOUR 
        WHERE (CITY ILIKE '%{standardized_city}%' 
        OR CITY ILIKE '%{standardized_city} United States%')
        """
        
        print(f"Executing tours query for city: {standardized_city}")
        cursor.execute(query)
        
        columns = [desc[0] for desc in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        results = convert_decimal_to_float(results)
        
        # Process tours to extract price values
        for tour in results:
            # Extract numeric price from the price string
            price_text = tour.get('PRICE', '')
            price_value = extract_price(price_text)
            tour['PriceValue'] = price_value
            
            # Convert rating to numeric
            if tour.get('RATING') and isinstance(tour.get('RATING'), str):
                try:
                    tour['RATING'] = float(tour['RATING'])
                except ValueError:
                    tour['RATING'] = 0
        
        # Filter tours based on budget
        if budget == "low":
            filtered_tours = [t for t in results if t.get('PriceValue', 0) <= 75]
        elif budget == "medium":
            filtered_tours = [t for t in results if 75 < t.get('PriceValue', 0) <= 200]
        else:  # high budget
            filtered_tours = [t for t in results if t.get('PriceValue', 0) > 200]
        
        # If we don't have enough tours in the budget range, include others
        if len(filtered_tours) < 5:
            # Sort all tours by price
            all_sorted = sorted(results, key=lambda x: x.get('PriceValue', 0))
            
            # Add appropriate tours based on budget
            if budget == "low" and all_sorted:
                filtered_tours = all_sorted[:min(10, len(all_sorted))]
            elif budget == "high" and all_sorted:
                filtered_tours = all_sorted[-min(10, len(all_sorted)):]
        
        # Sort by rating
        sorted_results = sorted(filtered_tours, 
                              key=lambda x: float(x.get('RATING', 0) or 0), 
                              reverse=True)
        
        print(f"Fetched {len(sorted_results)} tours for {standardized_city} with budget {budget}")
        return sorted_results
    
    except Exception as e:
        print(f"Error fetching tours: {e}")
        return []
    
    finally:
        if conn:
            conn.close()

def get_next_closest_places(current_url, all_places, category_type="attraction", max_results=3):
    # Different field mappings based on category type
    url_field = "URL"
    if category_type == "hotel":
        url_field = "LINK"  
        
    lat_field = "LATITUDE"
    lng_field = "LONGITUDE"
    
    # Find the current place details
    current_place = None
    for place in all_places:
        if place.get(url_field) == current_url:
            current_place = place
            break
            
 
    if not current_place:
        print(f"Current place with URL {current_url} not found")
        sorted_places = sorted(all_places, 
                             key=lambda x: float(x.get('RATING', 0) or 0), 
                             reverse=True)
        return sorted_places[:min(max_results, len(sorted_places))]
    
    
    try:
        if not all([current_place.get(lat_field), current_place.get(lng_field)]):
            # No coordinates, return top rated places
            print(f"Current place has no coordinates")
            sorted_places = sorted(all_places, 
                                 key=lambda x: float(x.get('RATING', 0) or 0), 
                                 reverse=True)
            filtered_places = [p for p in sorted_places if p.get(url_field) != current_url]
            return filtered_places[:min(max_results, len(filtered_places))]
    except:
        # Error checking coordinates, return top rated places
        print(f"Error checking coordinates for current place")
        sorted_places = sorted(all_places, 
                             key=lambda x: float(x.get('RATING', 0) or 0), 
                             reverse=True)
        filtered_places = [p for p in sorted_places if p.get(url_field) != current_url]
        return filtered_places[:min(max_results, len(filtered_places))]
    
    # Calculate distance to each place
    places_with_distances = []
    for place in all_places:
        # Skip the current place
        if place.get(url_field) == current_url:
            continue
            
        # Check if the place has valid coordinates
        try:
            if (place.get(lat_field) and place.get(lng_field) and
                isinstance(float(place.get(lat_field)), float) and 
                isinstance(float(place.get(lng_field)), float)):
                
                # Calculate distance
                distance = calculate_distance_between_attractions(current_place, place)
                places_with_distances.append((place, distance))
        except:
            # Skip places with invalid coordinates
            continue
    
    # If no places with valid coordinates, return top rated places
    if not places_with_distances:
        print(f"No places with valid coordinates found")
        sorted_places = sorted(all_places, 
                             key=lambda x: float(x.get('RATING', 0) or 0), 
                             reverse=True)
        filtered_places = [p for p in sorted_places if p.get(url_field) != current_url]
        return filtered_places[:min(max_results, len(filtered_places))]
    
    # Sort by distance (closest first)
    places_with_distances.sort(key=lambda x: x[1])
    
    # Return the closest places
    closest_places = [place[0] for place in places_with_distances[:max_results]]
    return closest_places

def is_attraction_free(attraction):
    """Determine if an attraction is free based on ticket details"""
    # Check ticket details field (updated column name)
    ticket_details = str(attraction.get('Ticket Details', '')).lower()
    
    # Keywords indicating free entry
    free_keywords = ['free', 'no charge', 'no fee', 'free entry', 'free admission', '$0']
    
    # Check for free keywords
    for keyword in free_keywords:
        if keyword in ticket_details:
            return True
    
    # Check if price has actual value
    price_value = extract_price_from_ticket_details(ticket_details)
    if price_value == 0 and ticket_details:
        return True
    
    # Default to not free
    return False

def extract_price_from_ticket_details(ticket_details):
    """Extract numeric price from ticket details text"""
    if not ticket_details:
        return 0
    
    # Look for price patterns
    price_patterns = [
        r'\$\s*(\d+(?:\.\d+)?)',  
        r'USD\s*(\d+(?:\.\d+)?)',  
        r'(\d+(?:\.\d+)?)\s*USD',  
        r'Adult(?:[^$])\$\s(\d+(?:\.\d+)?)', 
        r'Price(?:[^$])\$\s(\d+(?:\.\d+)?)'   
    ]
    
    for pattern in price_patterns:
        matches = re.findall(pattern, ticket_details)
        if matches:
            try:
                # Return the first price found
                return float(matches[0])
            except ValueError:
                continue
    
    return 0

def extract_price(price_text):
    """Extract numeric price from a price string"""
    if not price_text or not isinstance(price_text, str):
        return 0
    
    # Look for price patterns
    price_pattern = r'\$\s*(\d+(?:\.\d+)?)'
    usd_pattern = r'USD\s*(\d+(?:\.\d+)?)'   
    
    # Try dollar sign pattern
    dollar_matches = re.findall(price_pattern, price_text)
    if dollar_matches:
        try:
            return float(dollar_matches[0])
        except ValueError:
            pass
    
    # Try USD pattern
    usd_matches = re.findall(usd_pattern, price_text)
    if usd_matches:
        try:
            return float(usd_matches[0])
        except ValueError:
            pass
    
    # Try extracting any number
    number_pattern = r'(\d+(?:\.\d+)?)'
    number_matches = re.findall(number_pattern, price_text)
    if number_matches:
        try:
            return float(number_matches[0])
        except ValueError:
            pass
    
    return 0

def standardize_city_name(city):
    if not city:
        return ""
    
    city_lower = city.lower()
    
    # Handle common variations
    if "new york" in city_lower:
        return "New York"
    elif "san francisco" in city_lower:
        return "San Francisco"
    elif "los angeles" in city_lower:
        return "Los Angeles"
    elif "las vegas" in city_lower:
        return "Las Vegas"
    elif "chicago" in city_lower:
        return "Chicago"
    elif "seattle" in city_lower:
        return "Seattle"
    
    # Default: return the city name as-is
    return city

def sort_hotels_by_value(hotels, budget):
    # Calculate a value score for each hotel
    for hotel in hotels:
        rating = float(hotel.get('RATING', 3) or 3)
        price = hotel.get('PriceValue', 200)
        
        # Calculate a value score based on the budget
        if budget == "low":
            # For low budget, lower price is better
            price_score = max(0, 1 - (price / 300))  # 0 when price is 300+
            value_score = (rating * 0.6) + (price_score * 0.4)
        elif budget == "medium":
            # For medium budget, moderate price is better
            price_score = max(0, 1 - abs(price - 250) / 250)  # 1 when price is 250, decreases as it moves away
            value_score = (rating * 0.7) + (price_score * 0.3)
        else:  # high budget
            # For high budget, higher rating is most important, but price should be substantial
            price_score = min(1, price / 500)  # 1 when price is 500+
            value_score = (rating * 0.8) + (price_score * 0.2)
        
        hotel['ValueScore'] = value_score
    
    # Sort by the value score
    return sorted(hotels, key=lambda x: x.get('ValueScore', 0), reverse=True)

def calculate_distance_between_attractions(attraction1, attraction2):
    """Calculate the distance between two attractions using their coordinates"""
    # Check if coordinates are available
    if not all([attraction1.get('LATITUDE'), attraction1.get('LONGITUDE'), 
                attraction2.get('LATITUDE'), attraction2.get('LONGITUDE')]):
        return float('inf')  # Return infinity if coordinates not available
    
    try:
        # Convert to float and handle potential None values
        lat1 = float(attraction1.get('LATITUDE') or 0)
        lon1 = float(attraction1.get('LONGITUDE') or 0)
        lat2 = float(attraction2.get('LATITUDE') or 0)
        lon2 = float(attraction2.get('LONGITUDE') or 0)
        
        # Haversine formula
        R = 6371  # Earth radius in km
        dLat = math.radians(lat2 - lat1)
        dLon = math.radians(lon2 - lon1)
        a = (math.sin(dLat/2) * math.sin(dLat/2) + 
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * 
             math.sin(dLon/2) * math.sin(dLon/2))
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        distance = R * c
        
        return distance
    except (ValueError, TypeError) as e:
        print(f"Error calculating distance: {e}")
        return float('inf')

def get_nearby_attractions(attractions, num_attractions=3, max_distance=3.0):
    """Find groups of attractions that are close to each other"""
    if not attractions:
        return []
        
    if len(attractions) < num_attractions:
        return attractions[:min(num_attractions, len(attractions))]
    
    # Make sure all attractions have valid coordinates
    valid_attractions = []
    for attraction in attractions:
        try:
            if (attraction.get('LATITUDE') and attraction.get('LONGITUDE') and
                isinstance(float(attraction.get('LATITUDE')), float) and 
                isinstance(float(attraction.get('LONGITUDE')), float)):
                valid_attractions.append(attraction)
        except (ValueError, TypeError):
            continue
    
    if not valid_attractions:
        # If no valid coordinates, just return first few attractions
        return attractions[:min(num_attractions, len(attractions))]
    
    # Try to find attractions that are close to each other
    for i, anchor in enumerate(valid_attractions):
        nearby = [anchor]
        
        for j, candidate in enumerate(valid_attractions):
            if i == j:
                continue
                
            try:
                distance = calculate_distance_between_attractions(anchor, candidate)
                
                if distance <= max_distance:
                    nearby.append(candidate)
                    
                if len(nearby) >= num_attractions:
                    return nearby
            except Exception as e:
                print(f"Error in distance calculation: {e}")
                continue
                
    # If we couldn't find enough nearby attractions, return the first few valid ones
    return valid_attractions[:min(num_attractions, len(valid_attractions))]

def find_best_hotel_near_attractions(hotels, attractions):
    """Find the best hotel near a group of attractions"""
    if not hotels or not attractions:
        return None if not hotels else hotels[0]
    
    # Calculate center point of attractions
    valid_attractions = []
    for attraction in attractions:
        try:
            if (attraction.get('LATITUDE') and attraction.get('LONGITUDE') and
                isinstance(float(attraction.get('LATITUDE')), float) and 
                isinstance(float(attraction.get('LONGITUDE')), float)):
                valid_attractions.append(attraction)
        except (ValueError, TypeError):
            continue
    
    if not valid_attractions:
        # If no valid attractions with coordinates, just return highest rated hotel
        return max(hotels, key=lambda h: float(h.get('RATING', 0) or 0))
        
    avg_lat = sum(float(a.get('LATITUDE', 0) or 0) for a in valid_attractions) / len(valid_attractions)
    avg_lon = sum(float(a.get('LONGITUDE', 0) or 0) for a in valid_attractions) / len(valid_attractions)
    
    # Create a center point dict
    center = {'LATITUDE': avg_lat, 'LONGITUDE': avg_lon}
    
    # Score hotels based on distance and rating
    hotel_scores = []
    for hotel in hotels:
        # Ensure hotel has valid coordinates
        try:
            if not hotel.get('LATITUDE') or not hotel.get('LONGITUDE'):
                continue
                
            # Convert to float to verify they're valid numbers
            hotel_lat = float(hotel.get('LATITUDE'))
            hotel_lng = float(hotel.get('LONGITUDE'))
            
            distance = calculate_distance_between_attractions(center, hotel)
            rating = float(hotel.get('RATING', 3) or 3)
            
            # Score formula: weight rating more than distance
            # Normalize distance to 0-1 range (assuming max distance is 20km)
            normalized_distance = min(distance / 20, 1)
            
            # Normalize rating to 0-1 range (assuming 1-5 scale)
            normalized_rating = (rating - 1) / 4 if rating > 1 else 0
            
            # Calculate score (60% rating, 40% proximity)
            score = (normalized_rating * 0.6) + ((1 - normalized_distance) * 0.4)
            
            hotel_scores.append((hotel, score))
        except (ValueError, TypeError):
            # Skip hotels with invalid coordinates
            continue
    
    # If no hotels could be scored, just return the highest rated one
    if not hotel_scores:
        return max(hotels, key=lambda h: float(h.get('RATING', 0) or 0))
    
    # Sort by score (highest first)
    hotel_scores.sort(key=lambda x: x[1], reverse=True)
    
    return hotel_scores[0][0]

def find_nearby_free_attractions(paid_attractions, all_attractions, max_count=3):
    """Find free attractions near paid attractions"""
    if not paid_attractions or not all_attractions:
        return []
    
    # Filter to just free attractions
    free_attractions = [a for a in all_attractions if a.get('IsFree', False)]
    if not free_attractions:
        return []
    
    # Get center point of paid attractions
    valid_paid = []
    for attraction in paid_attractions:
        try:
            if (attraction.get('LATITUDE') and attraction.get('LONGITUDE') and
                isinstance(float(attraction.get('LATITUDE')), float) and 
                isinstance(float(attraction.get('LONGITUDE')), float)):
                valid_paid.append(attraction)
        except (ValueError, TypeError):
            continue
    
    if not valid_paid:
        return free_attractions[:max_count]  # No valid paid attractions, return any free ones
    
    # Calculate center
    center_lat = sum(float(a.get('LATITUDE', 0) or 0) for a in valid_paid) / len(valid_paid)
    center_lng = sum(float(a.get('LONGITUDE', 0) or 0) for a in valid_paid) / len(valid_paid)
    center = {'LATITUDE': center_lat, 'LONGITUDE': center_lng}
    
    # Calculate distances for all free attractions
    free_with_distances = []
    for attraction in free_attractions:
        try:
            if attraction.get('LATITUDE') and attraction.get('LONGITUDE'):
                distance = calculate_distance_between_attractions(center, attraction)
                free_with_distances.append((attraction, distance))
        except Exception:
            continue
    
    # Sort by distance
    free_with_distances.sort(key=lambda x: x[1])
    
    # Return the closest ones
    return [item[0] for item in free_with_distances[:max_count]]

# For testing
if __name__ == "_main__":
    # Test with a city
    test_city = "New York"
    test_budget = "medium"
    
    # Test attraction fetching with budget
    attractions = fetch_attractions(test_city, test_budget)
    print(f"Fetched {len(attractions)} attractions")
    
    # Print some sample attractions with price info
    for i, attraction in enumerate(attractions[:5]):
        print(f"Attraction {i+1}: {attraction.get('PLACENAME', 'Unknown')}")
        print(f"  Free: {attraction.get('IsFree', False)}")
        print(f"  Price: ${attraction.get('PriceValue', 0)}")
    
    # Test hotel fetching with budget
    hotels = fetch_hotels(test_city, test_budget)
    print(f"Fetched {len(hotels)} hotels")
    
    # Print top hotels with prices
    for i, hotel in enumerate(hotels):
        print(f"Hotel {i+1}: {hotel.get('NAME', 'Unknown')}")
        print(f"  Price: ${hotel.get('PriceValue', 0)}")
        print(f"  Rating: {hotel.get('RATING', 'Unknown')}")
    
    # Test tour fetching with budget
    tours = fetch_tours(test_city, test_budget)
    print(f"Fetched {len(tours)} tours")