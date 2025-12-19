import os
from datetime import datetime, timedelta
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from newsapi import NewsApiClient
from dotenv import load_dotenv

load_dotenv()

def get_market_sentiment(ticker: str):
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        return {"score": 0, "label": "Neutral (No Key)", "top_headlines": []}
    
    try:
        newsapi = NewsApiClient(api_key=api_key)
        start_date = (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d')
        
        response = newsapi.get_everything(q=ticker, from_param=start_date, language='en', sort_by='relevancy', page_size=10)
        articles = response.get('articles', [])
        
        if not articles: return {"score": 0, "label": "Neutral", "top_headlines": []}
        
        analyzer = SentimentIntensityAnalyzer()
        total_score = 0
        headlines = []
        
        for art in articles:
            title = art.get('title', '')
            if "[Removed]" in title: continue
            headlines.append(title)
            total_score += analyzer.polarity_scores(title)['compound']
            
        avg_score = total_score / len(headlines) if headlines else 0
        
        if avg_score > 0.15: label = "Bullish"
        elif avg_score < -0.15: label = "Bearish"
        else: label = "Neutral"
        
        return {
            "score": round(avg_score, 3),
            "label": label,
            "top_headlines": headlines[:3]
        }
    except Exception as e:
        return {"score": 0, "label": "Error", "top_headlines": [str(e)]}