import unittest
from datetime import datetime, timedelta
from data_fetcher.polygon_fetcher import PolygonFetcher

class TestPolygonFetcher(unittest.TestCase):
    def setUp(self):
        self.fetcher = PolygonFetcher()
        
    def test_get_historical_data(self):
        # Test fetching 1 day of 1-minute data
        import requests
        from requests.exceptions import Timeout

        try:
            data = self.fetcher.get_historical_data('SPY', '1m', 1)
        except Timeout:
            self.fail("API request timed out")
        
        # Basic validation
        self.assertGreater(len(data), 0)
        self.assertTrue(hasattr(data[0], 'timestamp'))
        self.assertTrue(hasattr(data[0], 'open'))
        self.assertTrue(hasattr(data[0], 'close'))
        
        # Verify timestamps are within expected range
        from datetime import timezone, timedelta
        eastern = timezone(timedelta(hours=-4))  # EDT offset
        now = datetime.now(timezone.utc)
        market_end = now.astimezone(eastern).replace(hour=16, minute=0, second=0, microsecond=0)
        market_start = (market_end - timedelta(days=1)).replace(hour=9, minute=30, second=0, microsecond=0)
        
        print(f"\nMarket start: {market_start}")
        print(f"Market end: {market_end}")
        
        for item in data:
            # Convert Polygon timestamp (milliseconds) to seconds
            item_timestamp = item.timestamp / 1000
            item_dt = datetime.fromtimestamp(item_timestamp, tz=timezone.utc)
            print(f"Data point: {item_dt} - {item}")
            
            self.assertGreaterEqual(item_timestamp, market_start.timestamp())
            self.assertLessEqual(item_timestamp, market_end.timestamp())

if __name__ == '__main__':
    unittest.main()