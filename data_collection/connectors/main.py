from worldnewsapi_connector import WorldNewsAPIConnector
import os
from dotenv import load_dotenv
load_dotenv()

def fetch_and_save_worldnews_data(api_key, query_text="supply_chain", num_months=12, num_results=100):
    """Fetch news data using the WorldNewsAPIConnector and save it to JSON and CSV formats."""
    
    # Derive meaningful filenames based on the query text and data source
    json_filename = f"data/worldnews_{query_text}_data.json"
    csv_filename = f"data/worldnews_{query_text}_data.csv"
    
    connector = WorldNewsAPIConnector(api_key)
    
    news_data = connector.fetch_monthly_news(text=query_text.replace("_", " "), num_months=num_months, num_results=num_results)
    connector.save_data_to_json(news_data, filename=json_filename)
    connector.convert_json_to_csv(json_file=json_filename, csv_file=csv_filename)
    
    return news_data

if __name__ == "__main__":
    API_KEY = os.environ.get("WORLDNEWS_API_KEY")
    query_text = "supply_chain"  # Using underscore as a separator for filenames
    
    news_data = fetch_and_save_worldnews_data(API_KEY, query_text=query_text, num_months=1, num_results=100)
    
    print(f"Total number of news articles related to '{query_text.replace('_', ' ')}' fetched: {len(news_data)}")
    print(f"Data has been successfully saved to 'worldnews_{query_text}_data.csv'")
