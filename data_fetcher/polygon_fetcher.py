import os
from datetime import datetime, timedelta
from polygon import RESTClient
import firebase_admin
from firebase_admin import credentials, db
import json
import os

# Initialize Firebase
cred = credentials.Certificate('firebase/serviceAccountKey.json')
if not firebase_admin._apps:
    print("Initializing Firebase...")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://apper-cb3d6-default-rtdb.firebaseio.com/'
    })
    print("Firebase initialized successfully")
from dotenv import load_dotenv

class PolygonFetcher:
    def store_in_firebase(self, ticker, timeframe, data):
        """Store historical data in Firebase"""
        ref = db.reference(f'/market_data/{ticker}/{timeframe}')
        for item in data:
            timestamp = item.timestamp
            ref.child(str(timestamp)).set({
                'open': item.open,
                'high': item.high,
                'low': item.low,
                'close': item.close,
                'volume': item.volume,
                'timestamp': item.timestamp
            })
    def __init__(self):
        load_dotenv()
        self.client = RESTClient(os.getenv('POLYGON_API_KEY'))
        
    def get_real_time_data(self, ticker='SPY'):
        """Fetch real-time SPY data and store in Firebase"""
        from datetime import datetime, timezone
        import time
        
        while True:
            try:
                # Get current timestamp
                now = datetime.now(timezone.utc)
                
                # Get real-time quote
                quote = self.client.get_real_time_quote(ticker)
                
                # Get options data
                options = self.client.get_options_chain(ticker)
                
                # Prepare data for Firebase
                data = {
                    'timestamp': now.isoformat(),
                    'spyPrice': quote.last_price,
                    'options': {
                        'calls': [option.last_price for option in options.calls],
                        'puts': [option.last_price for option in options.puts]
                    }
                }
                
                # Store in Firebase
                self.store_in_firebase(ticker, 'realtime', data)
                
                print("Fetched real-time data:", data)
                
                # Wait 1 minute before next update
                time.sleep(60)
                
            except Exception as e:
                print(f"Error fetching real-time data: {str(e)}")
                time.sleep(10)  # Wait 10 seconds before retrying