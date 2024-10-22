import tweepy
import yaml
import json
from datetime import datetime
from typing import Dict, List

class TwitterCollector :
    def __init__(self, config_path: str):
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)

        auth = tweepy.OAuthHandler(
            config['api_keys']['twitter']['api_key'],
            config['api_keys']['twitter']['api_secret']
        )
        auth.set_access_token(
            config['api_keys']['twitter']['access_token'],
            config['api_keys']['twitter']['access_token_secret']
        )
        self.api = tweepy.API(auth)
        self.client = tweepy.Client(
            bearer_token=config['api_keys']['twitter']['bearer_token']
        )

    def stream_tweets(self, keywords: List[str]) -> Dict:
        class TweetListener(tweepy.StreamingClient):
            def on_tweet(self, tweet):
                return {
                    'text': tweet.text,
                    'created_at': tweet.created_at.isoformat(),
                    'user_id': tweet.author_id,
                    'engagement_metrics': {
                        'retweets': tweet.public_metrics['retweet_count'],
                        'likes': tweet.public_metrics['like_count'],
                        'replies': tweet.public_metrics['reply_count']
                    }
                }

        stream = TweetListener(self.client.bearer_token)
        for keyword in keywords:
            stream.add_rules(tweepy.StreamRule(keyword))
        stream.filter()
        return stream

