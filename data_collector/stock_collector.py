import requests
import pandas as pd
from typing import Dict
import yaml

class StockCollector :
    def __init__(self, config_path: str):
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        self.api_key = config['api_keys']['alpha_vantage']['api_key']
        self.base_url = "https://www.alphavantage.co/query"

    def get_real_time_data(self, symbol: str) -> Dict:
        params = {
            'function': 'GLOBAL_QUOTE',
            'symbol': symbol,
            'apikey': self.api_key
        }
        response = requests.get(self.base_url, params=params)
        data = response.json()
        
        return {
            'symbol': symbol,
            'price': float(data['Global Quote']['05. price']),
            'volume': int(data['Global Quote']['06. volume']),
            'timestamp': data['Global Quote']['07. latest trading day']
        }


