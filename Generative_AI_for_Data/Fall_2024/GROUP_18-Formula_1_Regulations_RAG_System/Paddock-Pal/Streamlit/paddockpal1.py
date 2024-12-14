import os
import openai
from pinecone import Pinecone, ServerlessSpec
import streamlit as st
from dotenv import load_dotenv
import requests
from typing import List
from langchain.schema import HumanMessage, AIMessage
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_models import ChatOpenAI
from langchain.callbacks.tracers.langchain import LangChainTracer
from langchain.callbacks import tracing_enabled

# Load environment variables
load_dotenv()

# API Keys Setup
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENV")
NEWS_API_KEY = os.getenv("NEWSAPI_API_KEY")
LANGCHAIN_TRACING = os.getenv("LANGCHAIN_TRACING", "false")  # Set to "true" to enable tracing
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT", "paddock-pal-tracing")

# Validate environment variables
if not OPENAI_API_KEY or not PINECONE_API_KEY or not PINECONE_ENVIRONMENT or not NEWS_API_KEY:
    raise ValueError("API keys for OpenAI, Pinecone, or NewsAPI are missing.")

# Initialize Pinecone client
pinecone_client = Pinecone(api_key=PINECONE_API_KEY)

# Ensure Pinecone indexes exist
INDEX_NAMES = [
    "sporting-regulations-embeddings",
    "technical-regulations-embeddings",
    "financial-regulations-embeddings",
]
INDEX_HOSTS = {
    "sporting-regulations-embeddings": "sporting-regulations-embeddings-jl357j9.svc.ap-southeast-1.pinecone.io",
    "technical-regulations-embeddings": "technical-regulations-embeddings-jl357j9.svc.ap-southeast-1.pinecone.io",
    "financial-regulations-embeddings": "financial-regulations-embeddings-jl357j9.svc.ap-southeast-1.pinecone.io",
}

def ensure_index_exists(index_name, dimension=1536, metric="cosine"):
    if index_name not in pinecone_client.list_indexes().names():
        pinecone_client.create_index(
            name=index_name,
            dimension=dimension,
            metric=metric,
            spec=ServerlessSpec(cloud="aws", region=PINECONE_ENVIRONMENT),
        )
        print(f"Created index: {index_name}")
    else:
        print(f"Index {index_name} already exists.")

for index in INDEX_NAMES:
    ensure_index_exists(index)

def get_pinecone_index(index_name):
    """Retrieve Pinecone index by name."""
    return pinecone_client.Index(index_name)

# OpenAI setup
openai.api_key = OPENAI_API_KEY

def generate_embeddings_openai(text):
    try:
        response = openai.Embedding.create(
            input=text,
            model="text-embedding-ada-002"
        )
        return response["data"][0]["embedding"]
    except Exception as e:
        print(f"Error generating embeddings with OpenAI: {e}")
        return None

# Reflection and iterative improvement
def reflect_and_improve(query: str, context: str, iterations: int = 3) -> List[str]:
    """
    Use Reflection architecture to refine responses iteratively and return all responses.

    Parameters:
        query (str): User's question.
        context (str): Contextual information for the response.
        iterations (int): Number of reflection iterations.

    Returns:
        List[str]: A list of all responses generated during each iteration.
    """
    if not context:
        return ["No relevant information found in the database."]

    # Initialize the LLM
    llm = ChatOpenAI(model="gpt-4", temperature=0.7)

    # Define the generation and reflection prompts
    generation_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a highly knowledgeable assistant specializing in Formula 1 regulations."),
        ("user", f"Based on the following context, answer the question:\n\nContext:\n{context}\n\nQuestion:\n{query}")
    ])
    reflection_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert in Formula 1 regulations as well as a Formula 1 analyst. Your role is to provide constructive feedback and suggest improvements for clarity, context, and relevance in the answers."),
        MessagesPlaceholder(variable_name="messages")
    ])

    # Initial generation
    messages = [HumanMessage(content=query)]
    llm_responses = []

    for _ in range(iterations):
        # Generate response
        response = llm(messages).content

        # Save the response
        llm_responses.append(response)

        # Reflect on the response (not saved anymore)
        critique = reflection_prompt.invoke({"messages": [HumanMessage(content=query), AIMessage(content=response)]})
        critique_content = getattr(critique, 'content', str(critique))

        # Add response and critique to messages for the next iteration
        messages.append(AIMessage(content=response))
        messages.append(HumanMessage(content=critique_content))

    return llm_responses



def fetch_f1_news():
    """Fetch Formula 1-related news articles from NewsAPI."""
    url = f"https://newsapi.org/v2/everything?q=\"Formula 1\" OR F1&language=en&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            articles = response.json().get("articles", [])
            return [
                article for article in articles
                if "formula" in article["title"].lower() or "f1" in article["title"].lower()
            ]
        else:
            st.error(f"Error fetching news: {response.json().get('message')}")
            return []
    except Exception as e:
        st.error(f"Error fetching news: {str(e)}")
        return []

def display_news_section():
    """Display F1 News Section with hover effects."""
    st.markdown(
        """
        <style>
        .news-container {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            justify-content: center;
            padding: 20px;
        }
        .news-card {
            flex: 0 1 calc(33.333% - 20px);
            min-width: 300px;
            position: relative;
            overflow: hidden;
            border-radius: 15px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            background: white;
            transition: transform 0.3s ease;
        }
        .news-card img {
            width: 100%;
            height: 200px;
            object-fit: cover;
            border-radius: 15px 15px 0 0;
        }
        .news-card:hover {
            transform: translateY(-5px);
        }
        .news-content {
            padding: 15px;
        }
        .news-title {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 10px;
            color: #333;
        }
        .news-description {
            font-size: 14px;
            color: #666;
            margin-bottom: 15px;
            line-height: 1.4;
        }
        .read-more {
            display: inline-block;
            padding: 8px 16px;
            background-color: #E10600;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            transition: background-color 0.3s ease;
        }
        .read-more:hover {
            background-color: #B30500;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    articles = fetch_f1_news()

    if articles:
        st.markdown('<div class="news-container">', unsafe_allow_html=True)
        for article in articles[:9]:
            image = article.get("urlToImage", "")
            title = article.get("title", "No Title")
            description = article.get("description", "No description available.")
            url = article.get("url", "#")

            st.markdown(
                f"""
                <div class="news-card">
                    <img src="{image}" alt="{title}">
                    <div class="news-content">
                        <div class="news-title">{title}</div>
                        <div class="news-description">{description}</div>
                        <a href="{url}" target="_blank" class="read-more">Read More</a>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No news articles available at the moment.")

def fetch_relevant_documents(query: str):
    """Fetch relevant documents from Pinecone."""
    embedding = generate_embeddings_openai(query)
    if not embedding:
        raise ValueError("Failed to generate embedding for query.")

    all_results = []
    for index_name in INDEX_NAMES:
        index = get_pinecone_index(index_name)
        results = index.query(vector=embedding, top_k=5, include_metadata=True)
        all_results.extend(results["matches"])

    # Sort results by relevance score
    sorted_results = sorted(all_results, key=lambda x: x["score"], reverse=True)
    return sorted_results



def get_combined_context(matches: List[dict]) -> str:
    """Combine contexts from document matches."""
    seen_texts = set()
    contexts = []
    for match in matches:
        text = match["metadata"].get("text", "")
        if text and text not in seen_texts:
            seen_texts.add(text)
            contexts.append(text)
    return "\n\n".join(contexts[:3])

def generate_answer_with_openai(context, query):
    """
    Generate an answer for the query using OpenAI GPT-4 (Chat API), based on the given context.
    """
    if not context:
        return "No relevant information found in the database."

    messages = [
        {"role": "system", "content": "You are a knowledgeable assistant with expertise in Formula 1 regulations."},
        {"role": "user", "content": f"""Based on the following context, answer the question in detail. Provide a comprehensive response, include all relevant points, and elaborate wherever possible.

Context:
{context}

Question:
{query}"""}
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            max_tokens=5000,  # Increase the token limit
            temperature=0.7,
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"Error generating answer with OpenAI: {e}")
        return "An error occurred while generating the answer."

def show_paddockpal():
    st.write("Ask questions about Formula 1 regulations and get accurate answers!")

    query = st.text_input("Enter your question:", key="user_query")
    if st.button("Submit"):
        if not query.strip():
            st.warning("Please enter a valid question.")
        else:
            st.write("Processing your query...")

            # Step 1: Fetch relevant documents from Pinecone
            try:
                matches = fetch_relevant_documents(query)
                context = get_combined_context(matches)

                if not context:
                    st.warning("No relevant context found in Pinecone.")
                    return
            except Exception as e:
                st.error(f"Error fetching documents from Pinecone: {e}")
                return

            # Step 2: Generate an answer with OpenAI based on Pinecone's context
            st.subheader("Answer from Paddock Pal:")
            try:
                openai_answer = generate_answer_with_openai(context, query)
                st.markdown(
                    f"""
                    <div style="background-color: #F0F8FF; padding: 15px; border-radius: 10px; border: 1px solid #ADD8E6; margin-bottom: 15px;">
                        <p style="font-size: 16px; color: #333; line-height: 1.5;">{openai_answer}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            except Exception as e:
                st.error(f"Error generating OpenAI answer: {e}")
                return

            # Step 3: Generate iterative answers using LangChain's reflection process
            st.subheader("Iterative Answers from Reflection:")
            try:
                if LANGCHAIN_TRACING.lower() == "true":
                    tracer = LangChainTracer()
                    tracer.load_session(LANGCHAIN_PROJECT)

                    with tracing_enabled(tracer=tracer):
                        langchain_responses = reflect_and_improve(query, context, iterations=3)
                else:
                    langchain_responses = reflect_and_improve(query, context, iterations=3)

                # Display each response from LangChain iterations in styled cards
                for i, response in enumerate(langchain_responses, 1):
                    st.markdown(
                        f"""
                        <div style="border: 2px solid #4CAF50; border-radius: 10px; padding: 15px; margin-bottom: 15px; background-color: #E8F5E9;">
                            <h4 style="color: #4CAF50; margin-top: 0;">Iteration {i}</h4>
                            <p style="font-size: 16px; color: #333; line-height: 1.5;">{response}</p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
            except Exception as e:
                st.error(f"Error generating LangChain answers: {e}")


    # Display F1 News Section
    display_news_section()

def fetch_f1_news():
    """Fetch strictly F1-related news articles from NewsAPI."""
    url = f"https://newsapi.org/v2/everything?q=\"Formula 1\" OR F1&language=en&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            articles = response.json().get("articles", [])
            # Filter further if necessary to ensure relevance
            filtered_articles = [
                article for article in articles
                if "formula" in article["title"].lower() or "f1" in article["title"].lower()
            ]
            return filtered_articles
        else:
            st.error(f"Error fetching news: {response.json().get('message')}")
            return []
    except Exception as e:
        st.error(f"Error fetching news: {str(e)}")
        return []

def display_news_section():
    """Display a news section with hover effects and dynamic article details."""
    st.markdown(
        """
        <style>
        .news-container {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            justify-content: center;
            padding: 20px;
        }
        .news-card {
            flex: 0 1 calc(33.333% - 20px);
            min-width: 300px;
            position: relative;
            overflow: hidden;
            border-radius: 15px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            background: white;
            transition: transform 0.3s ease;
        }
        .news-card img {
            width: 100%;
            height: 200px;
            object-fit: cover;
            border-radius: 15px 15px 0 0;
        }
        .news-card:hover {
            transform: translateY(-5px);
        }
        .news-content {
            padding: 15px;
        }
        .news-title {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 10px;
            color: #333;
        }
        .news-description {
            font-size: 14px;
            color: #666;
            margin-bottom: 15px;
            line-height: 1.4;
        }
        .read-more {
            display: inline-block;
            padding: 8px 16px;
            background-color: #E10600;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            transition: background-color 0.3s ease;
        }
        .read-more:hover {
            background-color: #B30500;
        }
        @media (max-width: 992px) {
            .news-card {
                flex: 0 1 calc(50% - 20px);
            }
        }
        @media (max-width: 768px) {
            .news-card {
                flex: 0 1 100%;
            }
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    articles = fetch_f1_news()

    if articles:
        st.markdown('<div class="news-container">', unsafe_allow_html=True)
        for article in articles[:9]:
            image = article.get("urlToImage", "")
            title = article.get("title", "No Title")
            description = article.get("description", "No description available.")
            url = article.get("url", "#")

            st.markdown(
                f"""
                <div class="news-card">
                    <img src="{image}" alt="{title}">
                    <div class="news-content">
                        <div class="news-title">{title}</div>
                        <div class="news-description">{description}</div>
                        <a href="{url}" target="_blank" class="read-more">Read More</a>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No news articles available at the moment.")

if __name__ == "__main__":
    show_paddockpal()