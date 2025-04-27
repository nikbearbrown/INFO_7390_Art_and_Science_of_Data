import os
import json
import re

def load_all_json_files(folder_path):
    """
    Load all JSON files from a folder.
    """
    all_events = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                events = json.load(f)
                all_events.extend(events)
    return all_events

def clean_text(text):
    """
    Clean text by removing extra whitespace and unwanted characters.
    """
    if isinstance(text, list):
        text = ' '.join(text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def standardize_event(event):
    """
    Standardize a single event dictionary.
    """
    return {
        "title": clean_text(event.get("title", "No Title")),
        "date_time": clean_text(event.get("date_time", "No Date")),
        "location": clean_text(event.get("location", "Online Event")),
        "about": clean_text(event.get("about", "No Description")),
        "tags": clean_text(event.get("tags", [])),
        "event_link": event.get("event_link", "")
    }

def remove_duplicates(events):
    """
    Remove duplicate events based on (title + date_time + location).
    """
    seen = set()
    unique_events = []
    for event in events:
        identifier = (event['title'].lower(), event['date_time'].lower(), event['location'].lower())
        if identifier not in seen:
            seen.add(identifier)
            unique_events.append(event)
    return unique_events

def preprocess_events(input_folder, output_file):
    """
    Full preprocessing pipeline:
    - Load all events
    - Clean and standardize fields
    - Remove duplicates
    - Save cleaned events
    """
    # Load
    all_events = load_all_json_files(input_folder)
    print(f"Loaded {len(all_events)} events from {input_folder}")

    # Standardize
    cleaned_events = [standardize_event(event) for event in all_events]
    print(f"Standardized {len(cleaned_events)} events")

    # Remove Duplicates
    unique_events = remove_duplicates(cleaned_events)
    print(f"Removed duplicates. {len(unique_events)} unique events remain.")

    # Save
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(unique_events, f, indent=4, ensure_ascii=False)
    print(f"Saved cleaned events to {output_file} ✅")

if __name__ == "__main__":
    INPUT_FOLDER = "data"   # Raw scraped JSONs
    OUTPUT_FILE = "data/events_cleaned.json"

    preprocess_events(INPUT_FOLDER, OUTPUT_FILE)
