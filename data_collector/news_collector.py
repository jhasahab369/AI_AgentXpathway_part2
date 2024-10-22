import requests
import yaml
from typing import Dict, List
from datetime import datetime

class NewsCollector:
    def __init__(self, config_path: str):
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        self.api_key = config['api_keys']['news_api']['api_key']
        self.base_url = "https://newsapi.org/v2/everything"

    def get_news(self, keywords: List[str]) -> List[Dict]:
        params = {
            'q': ' OR '.join(keywords),
            'apiKey': self.api_key,
            'language': 'en',
            'sortBy': 'publishedAt'
        }
        response = requests.get(self.base_url, params=params)
        articles = response.json()['articles']

        return [{
            'title': article['title'],
            'content': article['content'],
            'source': article['source']['name'],
            'published_at': article['publishedAt']
        } for article in articles]


