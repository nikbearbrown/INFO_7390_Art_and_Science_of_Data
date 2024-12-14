import requests
from bs4 import BeautifulSoup

# URL of the target webpage
url = "https://www.geeksforgeeks.org/pandas-tutorial/"

# Fetch the webpage content
response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    # Remove unwanted navigation, similar reads, leftbar dropdowns, footer links, and hslider
    for unwanted in soup.find_all(class_=["header-main__wrapper", "similarReadDropdownItem", "leftbar-dropdown", "footer-wrapper_links"]):
        unwanted.decompose()
    hslider = soup.find('ul', id='hslider')
    if hslider:
        hslider.decompose()  # Remove the hslider section

    # Find the "Conclusion" heading and exclude everything after it
    conclusion_heading = soup.find('h2', text="Conclusion")
    if conclusion_heading:
        for sibling in conclusion_heading.find_next_siblings():
            sibling.decompose()  # Remove all siblings after "Conclusion"

    # Extract the title
    title = soup.find('h1').get_text(strip=True)
    title_keywords = [word.lower() for word in title.split()]  # Dynamically generate keywords from the title

    # Extract content while preserving structure
    content = []
    for element in soup.body.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'ol', 'ul'], recursive=True):
        if element.name == 'h1':
            content.append(f"\n# {element.get_text(strip=True)}\n")
        elif element.name == 'h2':
            content.append(f"\n## {element.get_text(strip=True)}\n")
        elif element.name == 'h3':
            content.append(f"\n### {element.get_text(strip=True)}\n")
        elif element.name == 'h4':
            content.append(f"\n#### {element.get_text(strip=True)}\n")
        elif element.name == 'p':
            content.append(f"{element.get_text(strip=True)}\n")
        elif element.name == 'ol':
            for idx, li in enumerate(element.find_all('li'), start=1):
                content.append(f"{idx}. {li.get_text(strip=True)}\n")
        elif element.name == 'ul':
            for li in element.find_all('li'):
                content.append(f"- {li.get_text(strip=True)}\n")

    # Scan the entire webpage for images and filter relevant ones dynamically
    images = soup.find_all('img')
    relevant_image_links = []
    for img in images:
        if 'src' in img.attrs:
            src = img['src']
            # Check if any title keyword matches the image link
            if any(keyword in src.lower() for keyword in title_keywords):
                relevant_image_links.append(src)

    # Save the structured content into a formatted text file
    with open("structured_data_science_details.txt", "w", encoding="utf-8") as file:
        # Title
        file.write(f"# {title}\n\n")

        # Webpage content
        file.writelines(content)

        # Relevant Images
        if relevant_image_links:
            file.write("\n## Relevant Image Links:\n")
            for link in relevant_image_links:
                file.write(f"{link}\n")
        else:
            file.write("\n## Relevant Image Links:\nNo relevant image links found.\n")

    print("All data has been successfully saved to 'structured_data_science_details.txt'")
else:
    print("Failed to fetch the webpage. Status code:", response.status_code)
