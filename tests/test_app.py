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
    assert b'SPY Price' in response.data
    assert b'Relative Strength Index (RSI)' in response.data

from firebase_admin import db

def test_firebase_connection():
    """Test Firebase connection"""
    # Initialize Firebase if not already initialized
    import firebase_admin
    from firebase_admin import credentials
    try:
        cred = credentials.Certificate('firebase/serviceAccountKey.json')
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://your-database-url.firebaseio.com/'
        }, name='test-app')
    except ValueError as e:
        if 'already exists' not in str(e):
            raise
    
    ref = db.reference('spy_options_test')
    assert ref is not None
    data = ref.get()
    assert data is not None, "Failed to fetch data from Firebase"
    assert isinstance(data, dict), "Firebase data should be a dictionary"