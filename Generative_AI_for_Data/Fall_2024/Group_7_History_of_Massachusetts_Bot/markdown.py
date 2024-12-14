import os
import pandas as pd

# Function to convert CSV files to Markdown
def csv_to_markdown(csv_folder_path, output_markdown_path):
    """
    Converts multiple CSV files to a single Markdown file.
    
    Parameters:
    - csv_folder_path (str): Path to the folder containing the CSV files.
    - output_markdown_path (str): Path to the output markdown file.
    """
    
    with open(output_markdown_path, 'w', encoding='utf-8') as md_file:
        
        # Loop through each CSV file in the folder
        for filename in os.listdir(csv_folder_path):
            
            if filename.endswith('.csv'):
                
                # Extract file name without extension for the main heading
                main_heading = os.path.splitext(filename)[0]
                
                # Write main heading to the markdown file
                md_file.write(f"# {main_heading}\n\n")
                
                # Read the CSV file
                csv_path = os.path.join(csv_folder_path, filename)
                df = pd.read_csv(csv_path)
                
                # Ensure required columns exist
                if 'section' in df.columns and 'text' in df.columns:
                    
                    for _, row in df.iterrows():
                        section_heading = row['section']
                        text_content = row['text']
                        
                        # Write section heading and text to markdown file
                        md_file.write(f"## {section_heading}\n\n")
                        md_file.write(f"{text_content}\n\n")
                else:
                    print(f"Warning: CSV file {filename} does not have 'section' and 'text' columns.")

    print(f"Markdown file created at {output_markdown_path}")

# Example usage
csv_folder_path = './raw_data/'  # Path to the folder containing CSV files
output_markdown_path = './raw_data/output.md'
csv_to_markdown(csv_folder_path, output_markdown_path)
