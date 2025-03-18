import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_route(client):
    """Test the index route returns a successful response"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Plotly Graph' in response.data
    assert b'plotly-graph' in response.data

def test_graph_data(client):
    """Test that the graph data is properly embedded in the response"""
    response = client.get('/')
    assert b'var graph = {' in response.data
    assert b'data' in response.data
    assert b'layout' in response.data
    assert b'SPY Options Data' in response.data

def test_firebase_connection():
    """Test Firebase connection"""
    ref = db.reference('spy_options_test')
    data = ref.get()
    assert data is not None, "Failed to fetch data from Firebase"
    assert isinstance(data, dict), "Firebase data should be a dictionary"