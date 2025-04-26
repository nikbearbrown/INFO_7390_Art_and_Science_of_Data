# backend/preprocessing.py

import pandas as pd
import os


def load_resume_data(filepath: str) -> pd.DataFrame:
    """Load resume data from a CSV file and clean HTML content."""
    df = pd.read_csv(filepath)
    df = df[["ID", "Resume_str", "Category"]].dropna()
    df = df.rename(columns={"Resume_str": "text", "Category": "label"})
    df["source"] = "resume"
    return df


def load_job_data(filepath: str) -> pd.DataFrame:
    """Load job description data from a CSV file."""
    df = pd.read_csv(filepath)
    df = df[["company_name", "job_description", "position_title"]].dropna()
    df["text"] = df["job_description"]
    df["label"] = df["position_title"]
    df["source"] = "job"
    df = df[["company_name", "text", "label", "source"]]
    return df


def merge_datasets(resume_df: pd.DataFrame, job_df: pd.DataFrame) -> pd.DataFrame:
    """Merge resume and job description data into one dataframe for embedding."""
    combined = pd.concat([resume_df[["text", "label", "source"]],
                          job_df[["text", "label", "source"]]], ignore_index=True)
    combined.drop_duplicates(subset="text", inplace=True)
    combined = combined[combined["text"].str.len() > 100]  # filter short entries
    return combined.reset_index(drop=True)


def save_processed_data(df: pd.DataFrame, output_path: str) -> None:
    """Save the cleaned and merged dataset."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Processed data saved to: {output_path}")


if __name__ == "__main__":
    resume_path = "../data/raw/Resume.csv"
    job_path = "../data/raw/training_data.csv"
    output_path = "../data/processed/merged_cleaned_dataset.csv"

    resumes = load_resume_data(resume_path)
    jobs = load_job_data(job_path)
    merged = merge_datasets(resumes, jobs)
    save_processed_data(merged, output_path)
