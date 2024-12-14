import wikipediaapi
import pandas as pd
import os
import tqdm

# Create a directory named 'raw_data' if it doesn't already exist
if not os.path.exists('raw_data'):
    os.makedirs('raw_data')

# Initialize a Wikipedia API object for English Wikipedia with a custom user-agent
wiki = wikipediaapi.Wikipedia('RAG 2 Riches', 'en', extract_format=wikipediaapi.ExtractFormat.WIKI)

def save_processed_csv(wiki, page_title, exclude_sections):
    """
    Fetches the content of a Wikipedia page, processes its sections recursively, 
    and saves the content to a CSV file while excluding specific sections.

    Parameters:
    - wiki: Wikipedia API object
    - page_title: The title of the Wikipedia page to process
    - exclude_sections: List of section titles to exclude from processing
    """
    # Get the Wikipedia page object
    wiki_page = wiki.page(page_title)
    try:
        # Check if the page exists; raise an error if it doesn't
        assert wiki_page.exists(), print("{} messed up".format(page_title))
    except:
        pass

    # Store processed section data
    data = []

    # Recursively process subsections of the Wikipedia page
    def process_final_subsections(section, full_title):
        # Construct the full section title
        full_title = full_title + ' -> ' + section.title if full_title else section.title
        
        # Skip excluded sections
        if section.title not in exclude_sections:
            # If no subsections exist, store the text
            if not section.sections:
                data.append({
                    'section': full_title,
                    'text': section.text
                })
            else:
                # Recursively process subsections
                for subsection in section.sections:
                    process_final_subsections(subsection, full_title)

    # Process all top-level sections of the page
    for s in wiki_page.sections:
        process_final_subsections(s, '')

    # Convert the data into a DataFrame and save it as a CSV file
    df = pd.DataFrame(data, columns=['section', 'text'])
    df.to_csv(os.path.join(os.path.curdir, 'raw_data/{}.csv'.format(page_title)), index=False)

# List of Wikipedia pages to process
page_names = [
    'History of Massachusetts', 'Massachusetts', 'Massachusetts Bay Colony',
    'History of slavery in Massachusetts', 'History of education in Massachusetts',
    'History of Springfield, Massachusetts', 'History of Boston', 
    'Outline of Massachusetts', 'Province of Massachusetts Bay'
]

# List of sections to exclude from processing
exclude_sections = [
    'See also', 'References', 'Bibliography', 
    'External links', 'Explanatory notes', 'Further reading'
]

# Process each page and save its content as a CSV file
for page in tqdm.tqdm(page_names):
    save_processed_csv(wiki, page, exclude_sections)

# Folder where all raw CSV files are stored
csv_folder = 'raw_data'

# List to store individual DataFrames for each CSV
dataframes = []

# Load all CSV files from the 'raw_data' folder
for file in os.listdir(csv_folder):
    if file.endswith('.csv'):
        file_path = os.path.join(csv_folder, file)
        df = pd.read_csv(file_path)  # Read each CSV as a DataFrame
        dataframes.append(df)       # Append to the list of DataFrames

# Combine all DataFrames into a single DataFrame
combined_df = pd.concat(dataframes, ignore_index=True)

# Save the combined DataFrame to a single CSV file
output_file = 'combined_data.csv'
combined_df.to_csv(output_file, index=False)

print(f"All files combined into {output_file}")
