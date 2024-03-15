from django.shortcuts import render
from scraper.news_scraper import scrape_bangla_news
from predictor.news_predictor import perform_bangla_sentiment

def save_data(request):
    # Scrape Bangla news headlines and articles
    title, description = scrape_bangla_news()
    print("Headline:", title, "\nArticle:", description)
    if title:
        for headline in title:
            headline_sentiment = perform_bangla_sentiment(headline)
            print("Headline Sentiment:", headline_sentiment)
    if description: 
        for article in description:
            article_sentiment = perform_bangla_sentiment(article)
            print("Article Sentiment:", article_sentiment)
    return render(request, 'success.html', {'Headline': title, 'Article': description, 'Headline Sentiment': headline_sentiment, 'Article Sentiment': article_sentiment})