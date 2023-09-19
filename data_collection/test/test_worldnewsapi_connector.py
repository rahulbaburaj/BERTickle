import pytest
from worldnewsapi_connector import WorldNewsAPIConnector
from unittest.mock import patch, Mock

def mock_requests_get(*args, **kwargs):
    class MockResponse:
        @staticmethod
        def json():
            return {"news": [{"title": "Sample News 1"}, {"title": "Sample News 2"}]}
    
    return MockResponse()

@pytest.fixture
def setup_connector():
    api_key = "mock_api_key"
    return WorldNewsAPIConnector(api_key)

def test_initialization(setup_connector):
    connector = setup_connector
    assert connector.api_key == "mock_api_key"

@patch("worldnewsapi_connector.WorldNewsAPIConnector.fetch_data", new=mock_requests_get)
def test_fetch_monthly_news(setup_connector):
    connector = setup_connector
    news_data = connector.fetch_monthly_news("supply chain", num_months=1, num_results=2)
    assert len(news_data) == 2
    assert news_data[0]["title"] == "Sample News 1"

def test_save_data_to_json(setup_connector, tmp_path):
    connector = setup_connector
    sample_data = [{"title": "Sample News 1"}, {"title": "Sample News 2"}]
    file_path = tmp_path / "test_news_data.json"
    connector.save_data_to_json(sample_data, filename=file_path)
    with open(file_path, 'r') as f:
        assert f.read() == '[{"title": "Sample News 1"}, {"title": "Sample News 2"}]'

def test_convert_json_to_csv(setup_connector, tmp_path):
    connector = setup_connector
    json_path = tmp_path / "test_news_data.json"
    csv_path = tmp_path / "test_news_data.csv"
    with open(json_path, 'w') as f:
        f.write('[{"title": "Sample News 1"}, {"title": "Sample News 2"}]')
    
    connector.convert_json_to_csv(json_path, csv_file=csv_path)
    with open(csv_path, 'r') as f:
        lines = f.readlines()
        assert lines[0] == ",title\n"
        assert lines[1] == "0,Sample News 1\n"
