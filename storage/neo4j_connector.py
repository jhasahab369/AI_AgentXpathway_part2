from neo4j import GraphDatabase
from typing import Dict
import yaml

class Neo4jConnector:
    def __init__(self, config_path: str):
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)

        self.driver = GraphDatabase.driver(
            config['neo4j']['uri'],
            auth=(config['neo4j']['user'], config['neo4j']['password'])
        )

    def store_sentiment(self, data: Dict):
        with self.driver.session() as session:
            session.run("""
                MERGE (p:Product {name: $product_name})
                CREATE (s:Sentiment {
                    score: $score,
                    confidence: $confidence,
                    timestamp: datetime($timestamp),
                    source: $source
                })
                CREATE (p)-[:HAS_SENTIMENT]->(s)
                """,
                product_name=data['product_name'],
                score=data['sentiment']['score'],
                confidence=data['sentiment']['confidence'],
                timestamp=data['timestamp'],
                source=data['source']
            )

    def store_trend(self, trend_data: Dict):
        with self.driver.session() as session:
            session.run("""
                MERGE (p:Product {name: $product_name})
                CREATE (t:Trend {
                    direction: $direction,
                    momentum: $momentum,
                    volatility: $volatility,
                    timestamp: datetime()
                })
                CREATE (p)-[:HAS_TREND]->(t)
                """,
                product_name=trend_data['product_name'],
                direction=trend_data['trend']['trend'],
                momentum=trend_data['trend']['momentum'],
                volatility=trend_data['trend']['volatility']
            )
