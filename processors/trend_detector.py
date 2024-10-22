import pandas as pd
import numpy as np
from typing import Dict, List

class TrendDetector:
    @staticmethod
    def detect_trends(data: pd.DataFrame) -> Dict:
        # Calculate moving averages
        data['MA5'] = data['score'].rolling(window=5).mean()
        data['MA20'] = data['score'].rolling(window=20).mean()
        
        # Calculate momentum
        data['momentum'] = data['score'].diff()
        
        # Detect trend direction
        current_trend = 'neutral'
        if data['MA5'].iloc[-1] > data['MA20'].iloc[-1]:
            current_trend = 'upward'
        elif data['MA5'].iloc[-1] < data['MA20'].iloc[-1]:
            current_trend = 'downward'
            
        return {
            'trend': current_trend,
            'momentum': data['momentum'].iloc[-1],
            'volatility': data['score'].std()
        }

