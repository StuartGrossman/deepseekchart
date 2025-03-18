import asyncio
import websockets
import json
import time

class TastytradeStreamer:
    def __init__(self, api_token):
        self.api_token = api_token
        self.ws_url = "wss://tasty-openapi-ws.dxfeed.com/realtime"
        self.connection = None
        self.channel_id = 1
        
    async def connect(self):
        self.connection = await websockets.connect(self.ws_url)
        await self._setup_connection()
        
    async def _setup_connection(self):
        # Step 1: SETUP
        setup_msg = {
            "type": "SETUP",
            "channel": 0,
            "version": "0.1-DXF-JS/0.3.0",
            "keepaliveTimeout": 60,
            "acceptKeepaliveTimeout": 60
        }
        await self.connection.send(json.dumps(setup_msg))
        
        # Step 2: AUTHORIZE
        auth_msg = {
            "type": "AUTH",
            "channel": 0,
            "token": self.api_token
        }
        await self.connection.send(json.dumps(auth_msg))
        
        # Step 3: Open channel
        channel_msg = {
            "type": "CHANNEL_REQUEST",
            "channel": self.channel_id,
            "service": "FEED",
            "parameters": {"contract": "AUTO"}
        }
        await self.connection.send(json.dumps(channel_msg))
        
    async def subscribe_to_spy(self):
        # Configure feed
        feed_setup = {
            "type": "FEED_SETUP",
            "channel": self.channel_id,
            "acceptAggregationPeriod": 0.1,
            "acceptDataFormat": "COMPACT",
            "acceptEventFields": {
                "Quote": ["eventType", "eventSymbol", "bidPrice", "askPrice", "bidSize", "askSize"]
            }
        }
        await self.connection.send(json.dumps(feed_setup))
        
        # Subscribe to SPY
        subscription_msg = {
            "type": "FEED_SUBSCRIPTION",
            "channel": self.channel_id,
            "reset": True,
            "add": [{
                "type": "Quote",
                "symbol": "SPY"
            }]
        }
        await self.connection.send(json.dumps(subscription_msg))
        
    async def start_stream(self):
        try:
            while True:
                message = await self.connection.recv()
                data = json.loads(message)
                print("Received:", data)
                
                # Send keepalive every 30 seconds
                if time.time() % 30 == 0:
                    keepalive = {"type": "KEEPALIVE", "channel": 0}
                    await self.connection.send(json.dumps(keepalive))
                    
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await self.connection.close()

async def main(api_token):
    streamer = TastytradeStreamer(api_token)
    await streamer.connect()
    await streamer.subscribe_to_spy()
    await streamer.start_stream()

if __name__ == "__main__":
    # Replace with your actual API token
    API_TOKEN = "your_api_token_here"
    asyncio.run(main(API_TOKEN))