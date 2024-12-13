import re
import PyPDF2


def extract_and_clean_pdf_text(pdf_path):
    """
    Extracts and cleans text from a PDF.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        str: Cleaned and filtered text content from the PDF.
    """
    cleaned_text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                page_text = page.extract_text()
                cleaned_lines = [
                    line for line in page_text.splitlines()
                    if not (
                        "Prerequisite(s)" in line or
                        "Corequisite(s)" in line or
                        "minimum grade of" in line or
                        ("of B-" in line.strip() and len(line.strip()) <= 10)
                    )
                ]
                normalized_lines = [line.replace("\u00A0", " ") for line in cleaned_lines]
                cleaned_text += "\n".join(normalized_lines) + "\n"
    except Exception as e:
        print(f"An error occurred: {e}")
    return cleaned_text


def extract_course_description(course_id, pdf_text):
    """
    Extracts course descriptions from cleaned PDF text.

    Args:
        course_id (str): The course ID to search for.
        pdf_text (str): The cleaned text content of the PDF.

    Returns:
        str: The course description.
    """
    start_index = pdf_text.find(course_id)
    if start_index != -1:
        subsequent_text = pdf_text[start_index:]
        match = re.search(r"\n(INFO|CSYE|DAMG)\s", subsequent_text)
        end_index = match.start() if match else len(subsequent_text)
        description = subsequent_text[:end_index]
        return description.split("\n", 1)[-1].strip()
    return "Description not found"
