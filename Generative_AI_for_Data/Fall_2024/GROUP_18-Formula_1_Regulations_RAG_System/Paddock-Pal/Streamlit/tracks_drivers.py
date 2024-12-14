import streamlit as st
import boto3
import os
from dotenv import load_dotenv
from io import BytesIO

# Load environment variables
load_dotenv()

# Initialize S3 client
@st.cache_resource
def init_s3_client():
    return boto3.client(
        's3',
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION")
    )

@st.cache_data
def load_section_data(bucket, section):
    """Load content and images for a specific section (Drivers/Tracks) from S3."""
    s3 = init_s3_client()
    try:
        data = {"items": []}
        response = s3.list_objects_v2(Bucket=bucket, Prefix=f"{section}/", Delimiter='/')
        if 'CommonPrefixes' in response:
            for prefix in response['CommonPrefixes']:
                item_name = prefix['Prefix'].split('/')[-2]
                data["items"].append(item_name)
                data["details"] = data.get("details", {})
                data["details"][item_name] = {"content": None, "image": None}
                try:
                    content_key = f"{section}/{item_name}/wiki_content.txt"
                    text_obj = s3.get_object(Bucket=bucket, Key=content_key)
                    content = text_obj['Body'].read().decode('utf-8')
                    data["details"][item_name]["content"] = content
                except Exception:
                    data["details"][item_name]["content"] = "No content available."
                try:
                    image_key = f"{section}/{item_name}/profile.jpg"
                    img_obj = s3.get_object(Bucket=bucket, Key=image_key)
                    image_data = BytesIO(img_obj['Body'].read())
                    data["details"][item_name]["image"] = image_data
                except Exception:
                    data["details"][item_name]["image"] = None
        elif 'Contents' in response:
            for obj in response['Contents']:
                key = obj['Key']
                if key.endswith("_info.txt"):
                    item_name = key.split('/')[-1].replace("_info.txt", "")
                    data["items"].append(item_name)
                    data["details"] = data.get("details", {})
                    data["details"][item_name] = {"content": None, "image": None}
                    try:
                        text_obj = s3.get_object(Bucket=bucket, Key=key)
                        content = text_obj['Body'].read().decode('utf-8')
                        data["details"][item_name]["content"] = content
                    except Exception:
                        data["details"][item_name]["content"] = "No content available."
                    try:
                        image_key = f"{section}/{item_name}_image.jpg"
                        img_obj = s3.get_object(Bucket=bucket, Key=image_key)
                        image_data = BytesIO(img_obj['Body'].read())
                        data["details"][item_name]["image"] = image_data
                    except Exception:
                        data["details"][item_name]["image"] = None
        return data
    except Exception as e:
        st.error(f"Error loading {section} data: {str(e)}")
        return None

def show_drivers_tracks():
    """Display Drivers and Tracks information with Load More functionality."""
    # Dropdown to choose between Drivers and Tracks
    category = st.selectbox("Choose a Category", ["Drivers", "Tracks"])

    # Load data for the selected category
    bucket = "f1wikipedia"
    data = load_section_data(bucket, category)

    if data and 'items' in data:
        selection = st.selectbox(f"Select a {category[:-1]}", data['items'])
        if selection:
            # Load initial 1% of the content
            content = data['details'][selection].get('content', 'No content available.')
            content_paragraphs = content.split("\n\n")
            total_paragraphs = len(content_paragraphs)

            # Initialize session state for loaded content
            if f"{selection}_loaded_paragraphs" not in st.session_state:
                st.session_state[f"{selection}_loaded_paragraphs"] = max(1, int(total_paragraphs * 0.01))

            # Display the currently loaded content
            image = data['details'][selection].get('image', None)
            with st.container():
                if image:
                    st.image(image, caption=f"{selection} Profile", use_container_width=True)

                for paragraph in content_paragraphs[:st.session_state[f"{selection}_loaded_paragraphs"]]:
                    st.markdown(paragraph)

                # Show "Load More" button if there's more content
                if st.session_state[f"{selection}_loaded_paragraphs"] < total_paragraphs:
                    if st.button(f"Load More {selection}"):
                        st.session_state[f"{selection}_loaded_paragraphs"] += max(1, int(total_paragraphs * 0.01))
                        st.rerun()
    else:
        st.warning(f"No data found for {category}. Please check your S3 bucket configuration.")

if __name__ == "__main__":
    show_drivers_tracks()
