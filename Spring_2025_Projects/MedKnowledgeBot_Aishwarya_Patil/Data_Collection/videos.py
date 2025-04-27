from googleapiclient.discovery import build
import pandas as pd
import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("youtube_api")

# Set up YouTube API
try:
    youtube = build('youtube', 'v3', developerKey=api_key)
    print("YouTube API client initialized successfully")
except Exception as e:
    print(f"Error initializing YouTube API client: {e}")
    exit(1)

def search_videos(query, max_results=10):
    """
    Search for videos on YouTube by query
    """
    videos = []
    
    try:
        # Search for videos
        search_response = youtube.search().list(
            q=query,
            part="snippet",
            maxResults=max_results,
            type="video",
            relevanceLanguage="en",
            safeSearch="moderate",
            videoEmbeddable="true",
            order="relevance"  # Other options: date, rating, viewCount
        ).execute()
        
        if 'items' not in search_response or len(search_response['items']) == 0:
            print(f"No videos found for query: {query}")
            return []
        
        for item in search_response['items']:
            try:
                video_id = item['id']['videoId']
                title = item['snippet']['title']
                description = item['snippet'].get('description', '')
                published_at = item['snippet'].get('publishedAt', '')
                channel_title = item['snippet'].get('channelTitle', '')
                
                # Get video details for duration, etc.
                video_response = youtube.videos().list(
                    part='contentDetails,statistics',
                    id=video_id
                ).execute()
                
                if 'items' in video_response and len(video_response['items']) > 0:
                    duration = video_response['items'][0]['contentDetails'].get('duration', '')
                    
                    # Handle missing statistics
                    if 'statistics' in video_response['items'][0]:
                        view_count = video_response['items'][0]['statistics'].get('viewCount', '0')
                    else:
                        view_count = '0'
                        
                    videos.append({
                        'video_id': video_id,
                        'title': title,
                        'description': description,
                        'published_at': published_at,
                        'duration': duration,
                        'view_count': view_count,
                        'channel': channel_title,
                        'url': f'https://www.youtube.com/watch?v={video_id}',
                        'search_query': query
                    })
                
                # Small delay between individual video requests
                time.sleep(0.2)
                
            except Exception as e:
                print(f"Error processing video: {e}")
                continue
                
    except Exception as e:
        print(f"Error in search_videos for query '{query}': {e}")
    
    return videos

# Create directories for output
os.makedirs('data', exist_ok=True)

# Medical topics to search for
topics = [
    'diabetes treatment medical',
    'cancer research medical',
    'cardiovascular disease medical',
    'infectious disease medical',
    'mental health treatment medical'
]

# List to store all videos
all_videos = []

# Process each topic
for topic in topics:
    print(f"\nSearching for '{topic}'...")
    
    try:
        # Get just 10 videos per topic
        topic_videos = search_videos(topic, max_results=10)
        
        if topic_videos:
            print(f"Found {len(topic_videos)} videos for '{topic}'")
            all_videos.extend(topic_videos)
            
            # Save topic-specific videos to CSV
            topic_df = pd.DataFrame(topic_videos)
            topic_csv_path = os.path.join('data', f'{topic.replace(" ", "_")}_videos.csv')
            topic_df.to_csv(topic_csv_path, index=False)
            print(f"Saved videos for '{topic}' to {topic_csv_path}")
        else:
            print(f"No videos found for '{topic}'")
        
        # Delay between topic searches to avoid hitting quota limits
        time.sleep(2)
        
    except Exception as e:
        print(f"Error processing topic '{topic}': {e}")
        continue

# Create DataFrame with all videos
if all_videos:
    all_videos_df = pd.DataFrame(all_videos)
    
    # Save to CSV
    main_csv_path = os.path.join('data', 'all_medical_videos.csv')
    all_videos_df.to_csv(main_csv_path, index=False)
    print(f"\nSaved {len(all_videos_df)} videos to {main_csv_path}")
else:
    print("No videos were found for any topic.")

print("\nScript execution completed.")