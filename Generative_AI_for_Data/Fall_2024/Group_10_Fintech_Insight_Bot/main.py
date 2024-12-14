import os
import streamlit as st
from streamlit_extras.let_it_rain import rain
import time
#from langchain import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import WebBaseLoader
from dotenv import load_dotenv
import yfinance as yf
import matplotlib.pyplot as plt
import feedparser #used for stock market news 
from nltk.sentiment import SentimentIntensityAnalyzer
from newspaper import Article  # Library to extract article text from URLs
from pinecone import Pinecone, ServerlessSpec
import pinecone
import openai
import nltk
nltk.download('punkt')
#from openai import OpenAI

# Load environment variables
load_dotenv()


# os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")
# openai_api_key = os.environ["OPENAI_API_KEY"]
openai_api_key= st.secrets["OPENAI_API_KEY"]

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7, max_tokens=300)
embeddings = OpenAIEmbeddings(api_key=openai_api_key)

# Pinecone setup
# os.environ['PINECONE_API_KEY'] = os.getenv("PINECONE_API_KEY")
# pinecone_api_key = os.environ["PINECONE_API_KEY"]
pinecone_api_key = st.secrets["PINECONE_API_KEY"]

index_name  = 'langchainvector1'
pc = Pinecone(api_key = pinecone_api_key)
index = pc.Index(index_name)
print("index-",index)

# Streamlit app setup
st.set_page_config(page_title="Fintech Insight Bot",page_icon="💰",)
st.markdown("<h1 style='text-align: center;'>Fintech Insight Bot 📊</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Empowering Users with Real-time Financial insights!</p>", unsafe_allow_html=True)
rain(emoji="💸", font_size=20, falling_speed=5) 

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select a page:", ["Insight Bot", "Real-time Stock Prices", "News Article Summarizer"])

if page == "Insight Bot":
    st.header("Insight Bot")
    st.sidebar.header("News Article URLs")
    number_of_urls = st.sidebar.number_input("Enter the number of URLs:", min_value=1, max_value=5, step=1, value=2)

    # Input URLs dynamically based on user input
    urls = []
    for i in range(number_of_urls):
        url = st.sidebar.text_input(f"URL {i+1}", key=f"url_{i+1}")
        if url:
            urls.append(url)

    process_url_clicked = st.sidebar.button("Process URLs")

    main_placeholder = st.empty()

    if process_url_clicked:
        if not urls:
            st.error("Please enter at least one URL.")
        else:
            # Load data using WebBaseLoader
            try:
                print("Data Loading... Started...")
                main_placeholder.text("Data Loading... Started... 💪")
                loader = WebBaseLoader(urls)
                data = loader.load()
                print("Data Loading... Completed!")
                main_placeholder.text("Data Loading... Completed! 🚀")

                # Split data into chunks
                text_splitter = RecursiveCharacterTextSplitter(separators=['\n\n', '\n', '.', ','], chunk_size=1000, chunk_overlap=50)
                
                print("Splitting Text into Chunks...")
                main_placeholder.text("Splitting Text into Chunks... 🔀")
                
                docs = text_splitter.split_documents(data)
                print("Splitting Text into Chunks... Completed.... ")
                
                time.sleep(2)

                print("Building Embedding Vectors...")
                main_placeholder.text("Building Embedding Vectors... 🌐")

                # adding embeddings to Pinecone
                data_to_upsert = []
                for i, doc in enumerate(docs):
                    vector = embeddings.embed_query(doc.page_content)
                    metadata = {"url": doc.metadata.get("source", "unknown"), "content": doc.page_content}
                    data_to_upsert.append((f"id-{i}", vector, metadata))

                # Upsert embeddings to Pinecone
                print("Upserting Data to Pinecone...")
                index.upsert(vectors=data_to_upsert)
                
                print("Upserting Data Completed!")
                main_placeholder.text("Upserting Data Completed! ✅")
            
                print("Embedding Vectors Saved Successfully!")
                main_placeholder.text("Embedding Vectors Saved Successfully! 🎉")
            except Exception as e:
                main_placeholder.text(f"Error: {e}")
                st.error(f"An error occurred while processing the URLs: {e}")

    # Input query for Q&A
    query = main_placeholder.text_input("First Process URLs. Ask a question about the processed articles:")
    if query:
        # if os.path.exists(file_path):
        try:
            print("Query-", query)
            query_vector = embeddings.embed_query(query)
            results = index.query(vector=query_vector, top_k=5, include_metadata=True)

            # Initialize an empty list to store the content and URL in a new dictionary
            content_url_list = []

            # Iterate through the results and extract the content and URL
            for match in results['matches']:
                content = match['metadata']['content']
                url = match['metadata']['url']
                
                # Create a new dictionary for each match with content and URL
                content_url_dict = {'content': content, 'url': url}
                
                # Append the dictionary to the list
                content_url_list.append(content_url_dict)

            # Now content_url_list contains all the dictionaries with content and URL
            print(content_url_list)
            # Generate the prompt for answering the question
            prompt = """Answer the following question based on the provided articles:\n + 
                    Answer the question based on the content, dont make things up from the internet 
                    ## Dont add your own predictions 
                    ### Please give complete senetences."""
            for entry in content_url_list:
                prompt += f"Content: {entry['content']}\nURL: {entry['url']}\n"
            prompt += f"\nQuestion: {query}\nAnswer:"

            # Generate the answer using OpenAI's GPT model
            # Using the OpenAI API with the "gpt-3.5-turbo" model
            # client = openai()

            # response = openai.ChatCompletion.create(
            #             model="gpt-3.5-turbo",
            #             prompt=prompt,
            #             max_tokens=100,
            #             temperature=0.7
            #             )
            # # Get the generated answer
            # answer = response.choices[0].text.strip()

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100,
                temperature=0.7
            )
            answer = response.choices[0].message["content"].strip()
            # Display answer
            st.header("Answer")
            st.write(answer)
        except Exception as e:
            st.error(f"An error occurred during the retrieval process: {e}")
    else:
        print("No data has been processed yet. Please process the URLs first.")

elif page == "Real-time Stock Prices":
    st.header("Real-time Stock Prices")
    stock_symbol = st.text_input("Enter a stock symbol (e.g., AAPL, TSLA, AMZN, META, UBER, CVS):")

    if stock_symbol:
        try:
            # Fetch stock data using yfinance
            stock_data = yf.Ticker(stock_symbol)
            print("------Stock Data-------")
            print(stock_data)
            # Try fetching stock history, if it fails, symbol might be incorrect
            stock_history = stock_data.history(period="5d")

            if stock_history.empty:
                raise ValueError("No data found for the entered stock symbol.")

            # Current price (latest close)
            stock_price = stock_history['Close'][-1]
            st.write(f"The current price of {stock_symbol.upper()} is **${stock_price:.2f}**")

            # Market Cap, P/E Ratio, and Sector
            market_cap = stock_data.info.get('marketCap', 'N/A')
            pe_ratio = stock_data.info.get('trailingPE', 'N/A')
            sector = stock_data.info.get('sector', 'N/A')

            st.subheader("Stock Information:")
            st.write(f"**Market Cap:** ${market_cap:,}")
            st.write(f"**P/E Ratio:** {pe_ratio}")
            st.write(f"**Sector:** {sector}")

            st.subheader("Related News:")
            news_url = f"https://news.google.com/rss/search?q={stock_symbol}"
            feed = feedparser.parse(news_url)
            if feed.entries:
                for entry in feed.entries[:5]:
                    st.markdown(f"[{entry.title}]({entry.link})")
                    st.caption(f"Published on: {entry.published}")
            else:
                st.write("No recent news available.")


        except ValueError as ve:
            st.error(f"{ve}. Please check for the correct stock symbol.")
        except Exception as e:
            st.error(f"An error occurred while fetching stock data: {e}. Please check the stock symbol and try again.")

elif page == "News Article Summarizer":
    # Streamlit application
    st.header("News Article Summarizer")

    # Input for the news article URL
    news_url = st.text_input("Enter a News Article URL:")

    if news_url:
        try:
            # Fetch the news article
            article = Article(news_url)

            article.download()
            article.parse()
            article.nlp()
        
            # Extract content
            news_content = article.text
            article_title = article.title
            article_summary = article.summary
            article_keywords = article.keywords

            if news_content:
                # Display the article's title
                st.subheader("Article Title")
                st.write(article_title)

                # Display article summary
                st.subheader("Article Summary")
                st.write(article_summary)

                # Display article keywords
                st.subheader("Article Keywords")
                st.write(", ".join(article_keywords))

            else:
                st.error("Could not extract content from the article. Please try another URL.")

        except Exception as e:
            st.error(f"An error occurred: {e}")
