from django.shortcuts import render
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import requests
from datetime import datetime
from .models import News

def fetch_news():
    """Fetch news from NewsAPI.org and save to database."""
    url = 'https://newsapi.org/v2/top-headlines'
    params = {
        'country': 'us',  # You can change this to get news from different countries
        'pageSize': 5,    # Number of articles to fetch
        'apiKey': settings.NEWS_API_KEY
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()

        if data.get('status') == 'ok':
            for article in data.get('articles', []):
                # Convert the published date string to datetime
                published_at = datetime.strptime(
                    article['publishedAt'], 
                    '%Y-%m-%dT%H:%M:%SZ'
                ).replace(tzinfo=timezone.utc)

                # Create or update the news article
                News.objects.update_or_create(
                    url=article['url'],
                    defaults={
                        'title': article['title'],
                        'description': article['description'] or '',
                        'image_url': article['urlToImage'],
                        'source_name': article['source']['name'],
                        'published_at': published_at,
                    }
                )
    except Exception as e:
        print(f'Error fetching news: {e}')

@login_required
def news_list(request):
    """Display the latest news articles."""
    # Fetch new articles before displaying
    fetch_news()
    
    # Get the latest 5 news articles
    news_articles = News.objects.all()[:5]
    
    return render(request, 'news/news_list.html', {
        'news_articles': news_articles,
        'show_news': True  # Used in template to show active tab
    })
