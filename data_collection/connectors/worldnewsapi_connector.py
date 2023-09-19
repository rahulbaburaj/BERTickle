from datetime import datetime, timedelta
from base_connector import BaseConnector
import json
import pandas as pd

class WorldNewsAPIConnector(BaseConnector):
    def __init__(self, api_key):
        endpoint = "https://api.worldnewsapi.com/search-news"
        headers = {
            "Content-Type": "application/json",
            # Add other necessary headers here if needed
        }
        super().__init__(endpoint, headers)
        self.api_key = api_key

    def fetch_monthly_news(self, text, num_months=12, num_results=100):
        params = {
            "text": text,
            "language": "en",
            "sort": "publish-time",
            "sort-direction": "DESC",
            "number": num_results,
            "api-key": self.api_key
        }

        all_news = []

        # Loop through the past specified number of months
        for i in range(num_months):
            start_date = datetime.now() - timedelta(days=(i+1)*30)
            end_date = datetime.now() - timedelta(days=i*30)
            
            params["earliest-publish-date"] = start_date.strftime('%Y-%m-%d %H:%M:%S')
            params["latest-publish-date"] = end_date.strftime('%Y-%m-%d %H:%M:%S')
            
            monthly_data = self.fetch_data(params)
            all_news.extend(monthly_data.get("news", []))

        return all_news

    def save_data_to_json(self, data, filename='news_data.json'):
        with open(filename, 'w') as outfile:
            json.dump(data, outfile)

    def convert_json_to_csv(self, json_file, csv_file='news_data.csv'):
        df = pd.read_json(json_file)
        df.to_csv(csv_file, index=False)
