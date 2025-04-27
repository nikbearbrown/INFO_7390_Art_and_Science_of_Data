# EventFinder AI — Personalized Search for Local Events

---

## 📌 Project Goals

- **Build an AI-powered RAG (Retrieval-Augmented Generation) system** to help users discover local events in Boston, MA.
- **Scrape real-world event data** from Eventbrite across multiple categories.
- **Preprocess and enrich event information** with tags like mood, theme, genre.
- **Embed events into a vector database** using OpenAI embeddings.
- **Enable a natural language and intent-based search interface** powered by Streamlit, ChromaDB, and OpenAI LLMs (GPT-3.5/4).
- **Summarize and recommend** events dynamically based on user queries.

---

## 🛠 Technologies Used

| Technology | Purpose |
|:---|:---|
| Python 3.10+ | Core Programming Language |
| aiohttp + BeautifulSoup | Web Scraping |
| Selenium (Headless Chrome) | Dynamic JavaScript Tag Extraction |
| OpenAI API | Text Embedding Generation + LLM Summarization |
| ChromaDB | Vector Database for Semantic Retrieval |
| Streamlit | Frontend UI for Search and Interaction |

---

## 📚 Folder Structure

```plaintext
EventFinder/
├── data/                      # Scraped and processed event data
│   ├── business_events.json
│   ├── music_events.json
│   ├── arts_events.json
│   └── ... (per category)
│
├── preprocessing/
│   ├── preprocess.py           # Cleans and standardizes event data
│   └── vector_embedding.py     # Embeds events into ChromaDB
│
├── scraper/
│   ├── scraper.py              # Scrapes event data (title, about, etc.)
│   ├── add_tags_to_events.py   # Selenium script to enrich events with tags
│
├── app/
│   └── main.py                 # Streamlit Search + LLM Summarization App
│
├── .env                        # OpenAI API Key Configuration
├── requirements.txt            # Python dependencies
└── README.md                   # Project Documentation
```

---

## 🛠 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/EventFinder.git
cd EventFinder
```

### 2. Create a Virtual Environment

```bash
python3 -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

### 3. Install Required Python Packages

```bash
pip install -r requirements.txt
```

Sample `requirements.txt`:

```
aiohttp
beautifulsoup4
selenium
chromadb
openai
python-dotenv
streamlit
```

✅ Ensure you have **Google Chrome** installed and **chromedriver** compatible with your browser version.

---

### 4. Setup Environment Variables

Create a `.env` file:

```plaintext
OPENAI_API_KEY=your_openai_api_key_here
```

---

## 🚀 Execution Instructions

### Step 1: Scrape Basic Event Data

```bash
python scraper/scraper.py
```

- Scrapes events across multiple categories.
- Saves data into `data/` folder.

---

### Step 2: Enrich Events with Tags

```bash
python scraper/add_tags_to_events.py
```

- Enriches each event by scraping dynamic "Tags" from Eventbrite event pages.

---

### Step 3: Preprocess and Clean Data

```bash
python preprocessing/preprocess.py
```

- Cleans, standardizes, and deduplicates events.

---

### Step 4: Generate Embeddings and Insert into ChromaDB

```bash
python preprocessing/vector_embedding.py
```

- Embeds event metadata using OpenAI embeddings and stores them in a persistent ChromaDB instance.

---

### Step 5: Launch the Streamlit Search App (LLM Integrated)

```bash
streamlit run app/main.py
```

- Semantic search with OpenAI embeddings
- Tag-based filtering
- LLM Summarization of matching events!

---

```markdown
## 🏛️ Architecture

![EventFinder AI Architecture](architecture_diag.png)
```

---

## 📈 Features

| Feature | Status |
|:---|:---|
| Scrape events from multiple categories | ✅ |
| Extract tags dynamically using Selenium | ✅ |
| Preprocess, clean, and deduplicate events | ✅ |
| Embed events into ChromaDB with OpenAI embeddings | ✅ |
| Semantic search by user queries | ✅ |
| Tag-based filtering for finer search control | ✅ |
| LLM-based event summarization and personalization | ✅ |
| Streamlit Frontend with black and green theme | ✅ |

---

## ✨ Example Usage Scenarios

- **Semantic Search Examples:**
  - "Fun dance parties this weekend for college students"
  - "Workshops to learn AI and data science near Boston"
  - "Family-friendly outdoor activities next week"

- **Tag Filtering Example:**
  - User selects `#danceparty`, `#hiphop`, then types "Saturday events" → finds matching parties.

- **User Intent Understanding:**
  - "I want to relax this weekend" → Recommends yoga, meditation events.
  - "I want to meet new people" → Finds networking events, mixers.

- **Summarized Output Example:**
  - Instead of raw event listings, the LLM summarizes matching events into a human-readable paragraph.

---

## 🙌 Acknowledgments

- [OpenAI](https://openai.com/) for embedding and LLM APIs.
- [ChromaDB](https://docs.trychroma.com/) team for building a high-speed vector database.
- [Streamlit](https://streamlit.io/) community for frontend development tools.
- [Eventbrite](https://eventbrite.com/) for providing public access to event data.

---

# 🚀 Final Words

**EventFinder AI** brings together scraping, vector search, and large language models into a single beautiful application.  
It helps users discover local events based on **semantic meaning**, **tags**, **user intent**, and **personalized summaries** — creating a smarter event discovery experience! 🚀🎉

Let's build smarter, human-centered AI systems!
