# Fintech_Insight_Bot📊

Welcome to the Fintech Insight Bot! This application leverages the power of Generative AI and cutting-edge NLP techniques to provide real-time financial insights. By using a Retrieval-Augmented Generation (RAG) approach, we’ve designed a bot that not only retrieves relevant data but also generates insightful, timely responses. Whether you’re looking for financial article summaries, stock market information, or intelligent Q&A about financial news, this bot has you covered.

With the integration of Pinecone Vector Database, we ensure efficient and accurate information retrieval, helping you make well-informed financial decisions.

Streamlit application - https://fintechinsightbot-nqgympkfgikwlzqfuft3a6.streamlit.app/

YouTube Link - https://www.youtube.com/watch?v=oDMjIS3Bya8

## Features

1. **Insight Bot:**
  - Processing and Indexing: We use Pinecone to process and index financial articles for fast, context-aware retrieval.
  - Smart Q&A System: Ask questions about the articles you process, and our bot will generate responses with relevant insights, thanks to OpenAI’s GPT models and embeddings.
  - Real-Time Financial Insights: Stay updated with real-time stock market data to enhance your financial decision-making process.

2. **Real-Time Stock Prices:**
  - Fetches stock prices using ```yfinance```.
  - View important market metrics like Market Cap, P/E ratio, and Sector for each stock.
  - Get related news articles to stay informed about the selected stock.

3. **News Article Summarizer:**
  - Simply provide a URL, and the bot will scrape and summarize the article for you using a web-based loader.
- It generates article keywords and a concise summary, making it easier to understand key points at a glance.

## Tech Stack

- Programming Language: Python
- Libraries:
  - LangChain for LLM chaining
  - OpenAI for GPT-based models
  - Pinecone for vector storage
  - Streamlit for the UI
  - ```yfinance``` for stock data
  - ```newspaper3k``` for news article processing
  - ```feedparser``` for RSS feeds
  - ```matplotlib``` for data visualization
  - ```nltk``` for sentiment analysis
- Environment: Streamlit web app
- Database: Pinecone

## Prerequisites

1. Python Environment: Ensure you have Python 3.8 or higher installed.
2. API Keys: Obtain the following API keys and set them in your environment variables:
    - OpenAI API Key
    - Pinecone API Key

3. Dependencies: Install required Python libraries using:
     ```pip install -r requirements.txt```

5. Environment Variables:
   - Create a .env file in the root directory with the following keys:
    ```
    OPENAI_API_KEY=your_openai_api_key
    PINECONE_API_KEY=your_pinecone_api_key
    
    ```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/your_username/fintech-insight-bot.git
   cd fintech-insight-bot
   
   ```

3. Install the dependencies:
  ```pip install -r requirements.txt```

4. Run the Streamlit app:
  ```streamlit run app.py```

## Usage

### Insight Bot

1. Navigate to the Insight Bot section.
2. Enter the URLs of articles to process.
3. Click on Process URLs to index the articles.
4. Ask questions about the processed articles in the query box.

### Real-Time Stock Prices

1. Navigate to the Real-Time Stock Prices section.
2. Enter the stock symbol (e.g., AAPL, TSLA).
3. View the stock price, market cap, P/E ratio, sector, and related news.

### News Article Summarizer

1. Navigate to the News Article Summarizer section.
2. Enter a URL for a news article.
3. View the extracted title, summary, and keywords of the article.

## File Structure
```
fintech-insight-bot/
├── app.py                # Main Streamlit application file
├── requirements.txt      # List of required Python packages
├── .env                  # Environment variables
├── config.toml           # Streamlit configuration
├── README.md             # Project documentation
```
## Streamlit Application

### Insight Bot

![image](https://github.com/user-attachments/assets/a8c6dcd7-583d-4d8c-ada4-2449d3049bea)
![image](https://github.com/user-attachments/assets/662077b2-1374-45d4-9123-cff409f4968c)

### Real-time Stock Prices

![image](https://github.com/user-attachments/assets/86c5b532-1878-4617-881a-7b44cd7682ed)

### News Article Summarizer

![image](https://github.com/user-attachments/assets/fec5ed3f-8520-41eb-b245-9f66405e4238)

## Future Improvements

1. Add support for more financial data APIs.
2. Optimize Pinecone indexing for faster retrieval.
3. Enhance the user interface for better usability.
4. Integrate sentiment analysis for financial news.


## License

This project is licensed under the MIT License.

## Acknowledgments

- [OpenAI](https://openai.com/) for GPT models
- [Pinecone](https://www.pinecone.io/) for vector storage
- [Streamlit](https://streamlit.io/) for building the app

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## Contact

For any inquiries, reach out at [Email](sameernimse99@gmail.com) or connect via [LinkedIn](https://www.linkedin.com/in/sameer522/).

