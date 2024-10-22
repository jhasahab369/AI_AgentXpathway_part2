import pathway as pw 
from typing import Dict, List
import json

class MarketingPipeline:
    def __init__(
            self,
            sentiment_analyzer,
            trend_detector,
            neo4j_connector,
            config_path: str
            ):
        self.sentiment_analyzer = sentiment_analyzer
        self.trend_detector = trend_detector
        self.neo4j_connector = neo4j_connector
        self.config_path = config_path

    def build_pipeline(self)-> pw.Table:
        social_data = pw.io.csv.read(
                "social_feed.csv"
                schema={
                    "text": str ,
                    "source": str ,
                    "created_at": str , 
                    "engagement": str
                    },
                mode= "streaming"
                )
        stock_data= pw.io.csv.read(
                "stock_feed.csv"
                schema = {
                    "symbol":str,
                    "price": float,
                    "volume": int , 
                    "timestamp": str
                    },
                mode= "streamin"
                )
        ews_data = pw.io.csv.read(
            "news_feed.csv",
            schema={
                "title": str,
                "content": str,
                "source": str,
                "published_at": str
            },
            mode="streaming"
        )

        # Process social media data
        processed_social = social_data.select(
            text=pw.this.text,
            source=pw.this.source,
            timestamp=pw.this.created_at,
            engagement=pw.this.engagement.apply(json.loads),
            sentiment=pw.this.text.apply(self.sentiment_analyzer.analyze)
        )

        processed_stocks = stock_data.select(
            symbol=pw.this.symbol,
            price=pw.this.price,
            volume=pw.this.volume,
            timestamp=pw.this.timestamp
        )

        # Process news data
        processed_news = news_data.select(
            title=pw.this.title,
            content=pw.this.content,
            source=pw.this.source,
            timestamp=pw.this.published_at,
            sentiment=pw.this.content.apply(self.sentiment_analyzer.analyze)
        )



        #now let us combine this all data as per pathway docs

        combined_data = pw.Table.concat([
            processed_social.select(
                type="social",
                score=pw.this.sentiment.apply(lambda x: x['score']),
                timestamp=pw.this.timestamp
            ),
            processed_stocks.select(
                type="stock",
                score=pw.this.price,
                timestamp=pw.this.timestamp
            ),
            processed_news.select(
                type="news",
                score=pw.this.sentiment.apply(lambda x: x['score']),
                timestamp=pw.this.timestamp
            )
        ])

        trends = combined_data.windowby(
            pw.temporal.sliding_window(
                duration=pw.temporal.duration("1h"),
                stride=pw.temporal.duration("5m")
            ),
            lambda window, data: data.reduce(
                avg_score=pw.reducers.avg(pw.this.score),
                count=pw.reducers.count(),
                start_time=pw.reducers.min(pw.this.timestamp),
                end_time=pw.reducers.max(pw.this.timestamp)
            )
        )

        trends.sink(pw.io.python.callback(self.neo4j_connector.store_trend))

        return trends



















