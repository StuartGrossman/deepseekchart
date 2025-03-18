import unittest
from app import app
import numpy as np

class TestRSIFrontend(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_rsi_data_passed_to_frontend(self):
        # Test with sample data
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        
        # Check if RSI data is in the response
        html_content = response.data.decode('utf-8')
        self.assertIn('var graph =', html_content)
        
        # Extract RSI values from the response
        import re
        import json
        graph_data = re.search(r'var graph = (.*?);', html_content)
        self.assertIsNotNone(graph_data, "Graph data not found in response")
        
        # Parse the graph data
        graph_json = json.loads(graph_data.group(1))
        rsi_trace = next(trace for trace in graph_json['data'] if trace['name'] == 'RSI')
        rsi_values = rsi_trace['y']
        
        print("\nRSI Values passed to frontend:", rsi_values)
        
        # Verify RSI values are within expected range
        self.assertTrue(all(0 <= value <= 100 for value in rsi_values))

if __name__ == '__main__':
    unittest.main()