import yaml
from data_collectors import TwitterCollector, StockCollector, NewsCollector
from processors import SentimentAnalyzer, TrendDetector
from storage import Neo4jConnector
from pipeline import MarketingPipeline

def main():
    # Initialize components
    config_path = "config/config.yaml"
    
    # Initialize collectors
    twitter_collector = TwitterCollector(config_path)
    stock_collector = StockCollector(config_path)
    news_collector = NewsCollector(config_path)
    
    # Initialize processors
    sentiment_analyzer = SentimentAnalyzer()
    trend_detector = TrendDetector()
    
    # Initialize storage
    neo4j_connector = Neo4jConnector(config_path)
    
    # Initialize pipeline
    pipeline = MarketingPipeline(
        sentiment_analyzer,
        trend_detector,
        neo4j_connector,
        config_path
    )
    
    # Set up data collection
    keywords = ["your_product", "competitor_product"]
    
    # Start collectors
    twitter_stream = twitter_collector.stream_tweets(keywords)
    stock_data = stock_collector.get_real_time_data("AAPL")  # example stock
    news_data = news_collector.get_news(keywords)
    
    # Build and run pipeline
    trends = pipeline.build_pipeline()
    
    # Run the pathway engine
    pw.run()

if __name__ == "__main__":
    main()
