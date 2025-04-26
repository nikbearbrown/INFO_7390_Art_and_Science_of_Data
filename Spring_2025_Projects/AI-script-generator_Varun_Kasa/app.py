import streamlit as st
import openai
import os
import base64
from io import BytesIO
import requests
from PIL import Image
from gtts import gTTS
from moviepy.editor import ImageSequenceClip, AudioFileClip
import tempfile

# Configure Streamlit page
st.set_page_config(
    page_title="🎬 Script & Storyboard Generator",
    layout="wide",
    page_icon="🎥"
)

# Custom CSS for theme and layout
st.markdown("""
<style>
    .stApp {
        background-color: #0E1117;
        color: white;
    }
    .title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .footer {
        text-align: center;
        margin-top: 3rem;
        font-size: 0.9rem;
        color: gray;
    }
    .section {
        background-color: #161A25;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🎬 AI-Powered Script & Storyboard Generator</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter your OpenAI API Key", type="password")
    if api_key:
        openai.api_key = api_key
        st.success("API Key set successfully!")

    st.markdown("""
    ### About
    This app uses GPT-4o to generate creative scripts and DALL·E 3 for storyboards.
    Made by **Varun Kasa** using Streamlit and OpenAI.
    """)

# Input fields
st.markdown('<div class="section">', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    genre1 = st.selectbox("Primary Genre", ["Sci-Fi", "Romance", "Action", "Comedy", "Drama", "Horror", "Thriller", "Fantasy", "Mystery", "Adventure"])
with col2:
    genre2 = st.selectbox("Secondary Genre", ["None", "Sci-Fi", "Romance", "Action", "Comedy", "Drama", "Horror", "Thriller", "Fantasy", "Mystery", "Adventure"])

num_characters = st.slider("Number of Characters", 2, 5, 3)
character_names = [st.text_input(f"Character {i+1} Name", value=f"Character {i+1}") for i in range(num_characters)]
premise = st.text_area("Story Premise", height=150)
generate_storyboard = st.checkbox("Generate storyboard images", value=True)
generate_video = st.checkbox("Generate video narration with storyboards", value=False)

st.markdown('</div>', unsafe_allow_html=True)

if st.button("Generate Script"):
    if not api_key:
        st.error("API Key is required")
    elif not premise.strip():
        st.error("Premise cannot be empty")
    else:
        genres = genre1 if genre2 == "None" else f"{genre1} and {genre2}"
        characters_str = ", ".join(character_names)

        base_prompt = f"""
        Write a 5-page movie script in {genres} style.
        Characters: {characters_str}
        Premise: {premise}
        Format with proper screenplay structure.
        Each page should start with 'PAGE 1', 'PAGE 2', etc.
        """

        with st.spinner("Generating script..."):
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a professional screenwriter."},
                    {"role": "user", "content": base_prompt}
                ],
                max_tokens=4000,
                temperature=0.8
            )
            script = response.choices[0].message.content
            st.session_state.script = script
            st.success("Script generated successfully!")

        st.subheader("📄 Generated Script")
        st.code(script, language="markdown")

        with st.spinner("Generating logline and synopsis..."):
            summary_prompt = f"Generate a logline and 1-paragraph synopsis for the following movie script:\n{script}"
            summary_response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": summary_prompt}],
                temperature=0.7,
                max_tokens=500
            )
            st.info(summary_response.choices[0].message.content)

        with st.expander("🎭 Character Descriptions"):
            for name in character_names:
                char_prompt = f"Describe the character '{name}' from this script, including personality, age, and background:\n{script}"
                char_response = openai.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": char_prompt}],
                    temperature=0.6,
                    max_tokens=250
                )
                st.markdown(f"**{name}**")
                st.write(char_response.choices[0].message.content)

        if generate_storyboard:
            st.subheader("🎞️ Storyboard Preview")
            script_pages = [pg for pg in script.split("PAGE") if pg.strip()][:5]
            img_cols = st.columns(5)
            images = []

            for i, pg in enumerate(script_pages):
                image_prompt = f"Storyboard illustration in {genres} style showing: {pg.strip()[:400]}"
                img_response = openai.images.generate(
                    model="dall-e-3",
                    prompt=image_prompt,
                    size="1024x1024",
                    quality="standard",
                    n=1
                )
                img_url = img_response.data[0].url
                img_data = requests.get(img_url).content
                images.append(img_data)
                img = Image.open(BytesIO(img_data))
                with img_cols[i % 5]:
                    st.image(img, caption=f"Page {i+1}", use_container_width=True)

            if generate_video:
                st.subheader("📽️ Narrated Video")
                tts = gTTS(text=script, lang='en')
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tts_fp:
                    tts.save(tts_fp.name)
                    audio_path = tts_fp.name

                with tempfile.TemporaryDirectory() as tmpdir:
                    frame_paths = []
                    for idx, img_data in enumerate(images):
                        img_path = os.path.join(tmpdir, f"frame_{idx}.png")
                        with open(img_path, 'wb') as f:
                            f.write(img_data)
                        frame_paths.append(img_path)

                    clip = ImageSequenceClip(frame_paths, fps=1)
                    audio = AudioFileClip(audio_path)
                    final = clip.set_audio(audio)

                    video_path = os.path.join(tmpdir, "output_video.mp4")
                    final.write_videofile(video_path, codec="libx264", audio_codec="aac")

                    with open(video_path, "rb") as file:
                        st.download_button("🎬 Download Narrated Video", file.read(), file_name="script_video.mp4")

        st.download_button("📩 Download Script", data=script, file_name="script.txt")

st.markdown('<div class="footer">Made with ❤️ by Varun Kasa · Powered by OpenAI</div>', unsafe_allow_html=True)
