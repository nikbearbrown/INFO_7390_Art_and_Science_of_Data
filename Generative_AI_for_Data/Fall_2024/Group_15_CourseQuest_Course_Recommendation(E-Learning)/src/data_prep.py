import pandas as pd
import re
import json
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import os

# Text preprocessing function
def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove non-alphanumeric characters
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text).strip()
    # Tokenize and remove stopwords
    stop_words = set(stopwords.words("english"))
    tokens = word_tokenize(text)
    return " ".join([word for word in tokens if word not in stop_words])

# Preprocess CSV and save as JSON
def preprocess_csv(input_csv_path, output_json_path):
    # Read the CSV file
    data = pd.read_csv(input_csv_path)
    
    # Preprocess text fields
    for col in data.columns:
        if data[col].dtype == "object":  # Only process string columns
            data[col] = data[col].apply(lambda x: preprocess_text(str(x)) if pd.notnull(x) else x)

    # Save preprocessed data to JSON
    data.to_json(output_json_path, orient="records", indent=4)
    print(f"Preprocessed data saved to {output_json_path}")

# Example usage
if __name__ == "__main__":
    input_csv = "D:/Adv. Data Science Project/data/raw/CourseraDataset-Clean.csv"  # Replace with your CSV path
    output_json = "D:/Adv. Data Science Project/data/processed/preprocessed_data.json"
    
    # Download stopwords if not already available
    import nltk
    nltk.download("stopwords")
    nltk.download("punkt")
    
    preprocess_csv(input_csv, output_json)
