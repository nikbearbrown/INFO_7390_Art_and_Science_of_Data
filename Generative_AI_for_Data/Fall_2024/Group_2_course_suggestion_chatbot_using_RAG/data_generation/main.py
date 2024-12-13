from scraper import scrape_iframe_page
from pdf_handler import extract_and_clean_pdf_text, extract_course_description
from data_generation.utils import save_to_csv, save_to_txt
import pandas as pd

def main():
    # Scrape courses
    main_url = 'http://newton.neu.edu/spring2025/'
    courses_df = scrape_iframe_page(main_url)
    if courses_df.empty:
        print("No course data found.")
        return

    # Modify DataFrame
    courses_df['CourseID'] = courses_df['Course Name'].str.extract(r'(^[A-Z]+ \d{4})')
    courses_df['Course Name'] = courses_df['Course Name'].str.replace(r'^[A-Z]+ \d{4}-\d{2} ', '', regex=True)

    # Extract and clean PDF text
    pdf_path = "./input/CourseDescriptions.pdf"
    cleaned_text = extract_and_clean_pdf_text(pdf_path)
    save_to_txt(cleaned_text, "./output/CleanedCourseDescriptions.txt")

    # Extract course descriptions
    courses_df["Course Description"] = courses_df["CourseID"].apply(
        lambda x: extract_course_description(x, cleaned_text)
    )

    # Save to CSV
    save_to_csv(courses_df, "./output/ExtractedCourseDescriptions.csv")


if __name__ == "__main__":
    main()
