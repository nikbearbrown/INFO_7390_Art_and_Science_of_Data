# Social Sentiment Analysis Agent for Stock Market Prediction

![Stock Sentiment Dashboard](https://via.placeholder.com/800x400?text=Stock+Sentiment+Dashboard)

## Project Overview

This project implements a stock market prediction system that analyzes market sentiment using financial news and technical indicators to forecast potential stock price movements. The application provides a user-friendly interface for investors to make more informed trading decisions based on both sentiment analysis and technical signals.

### Features

- **Stock Data Visualization**: View historical price charts with moving averages
- **Sentiment Analysis**: Analyze market sentiment from multiple financial sources
- **Technical Analysis**: Incorporate price trends and moving average indicators
- **Combined Prediction**: Generate forecasts based on both sentiment and technical signals
- **Interactive Dashboard**: User-friendly interface built with Streamlit

## Technology Stack

- **Python**: Core programming language
- **Streamlit**: Web application framework
- **yfinance**: Yahoo Finance API for historical stock data
- **pandas & numpy**: Data manipulation and analysis
- **matplotlib**: Data visualization
- **Beautiful Soup**: Web scraping for financial news
- **Natural Language Processing**: Sentiment analysis of financial news

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/stock-sentiment-predictor.git
cd stock-sentiment-predictor
```

2. Create a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install required packages
```bash
pip install -r requirements.txt
```

### Running the Application

1. Start the Streamlit server
```bash
streamlit run app.py
```

2. Open your browser and navigate to `http://localhost:8501`

## How to Use

1. Enter a stock ticker symbol in the sidebar (e.g., AAPL, MSFT, TSLA)
2. Select the number of days of historical data you want to analyze
3. Click the "Analyze" button to process the data
4. View the prediction results, sentiment analysis, and stock chart
5. Explore the sentiment scores from different sources and the latest news

## Project Structure

```
stock-sentiment-predictor/
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
└── data/                  # Sample data and model files (optional)
```

## How It Works

### 1. Data Collection

The application fetches historical stock price data using the Yahoo Finance API (yfinance). It also simulates sentiment data from various financial sources like MarketBeat, TipRanks, Macroaxis, and others.

### 2. Sentiment Analysis

The system analyzes sentiment from multiple financial sources, providing a weighted sentiment score that reflects the market's overall outlook on a particular stock. In a production environment, this would connect to real sentiment API providers or implement web scraping of financial news.

### 3. Technical Analysis

Basic technical indicators are calculated from the historical stock data:
- Short-term and long-term moving averages (5-day and 20-day)
- Price change percentage over recent periods

### 4. Prediction Model

The prediction model combines:
- Technical signals (60% weight): Based on moving average crossovers and recent price trends
- Sentiment signals (40% weight): Aggregated from financial news and market sentiment sources

The final prediction provides:
- Direction (up/down)
- Confidence level
- Individual contributions from technical and sentiment components

## Future Improvements

- Implement real-time sentiment analysis from Twitter and other social media
- Add more advanced technical indicators (RSI, MACD, Bollinger Bands)
- Incorporate machine learning models for improved prediction accuracy
- Develop alert systems for significant sentiment shifts
- Add portfolio tracking and management features
- Implement backtesting to evaluate prediction performance

## Requirements

```
streamlit==1.30.0
pandas==2.0.3
numpy==1.24.3
matplotlib==3.7.2
yfinance==0.2.35
requests==2.31.0
beautifulsoup4==4.12.2
```

## Contributors

- [Your Name](https://github.com/yourusername)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Yahoo Finance for providing free stock data API
- Streamlit for the excellent web application framework
- Financial sentiment analysis research and methodologies

---

*Note: This application is for educational purposes only and should not be used for actual investment decisions. Always consult with a financial advisor before making investment choices.*
