from transformers import pipeline
from typing import Dict, Union
import numpy as np

class SentimentAnalyzer:
    def __init__(self):
        self.analyzer = pipeline(
            "sentiment-analysis",
            model="finiteautomata/bertweet-base-sentiment-analysis"
        )

    def analyze(self, text: str) -> Dict[str, Union[str, float]]:
        try:
            result = self.analyzer(text)[0]
            score = float(result['score'])
            if result['label'] == 'NEG':
                score = -score
            return {
                'score': score,
                'confidence': abs(score),
                'label': result['label']
            }
        except Exception:
            return {
                'score': 0.0,
                'confidence': 0.0,
                'label': 'NEUTRAL'
            }
