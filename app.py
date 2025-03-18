from flask import Flask, render_template_string
import plotly.graph_objs as go
import plotly
from plotly.subplots import make_subplots
import firebase_admin
from firebase_admin import credentials, db
from firebase.config import FIREBASE_CONFIG
import numpy as np

def calculate_rsi(prices, period=14):
    """Calculate Relative Strength Index (RSI)"""
    deltas = np.diff(prices)
    seed = deltas[:period + 1]
    up = seed[seed >= 0].sum() / period
    down = -seed[seed < 0].sum() / period
    
    # Handle flat prices (no change)
    if down == 0:
        # If all prices are increasing, RSI should be 100
        if np.all(deltas > 0):
            return np.full_like(prices, 100)
        # If all prices are flat, RSI should be 50
        if np.all(deltas == 0):
            return np.full_like(prices, 50)
        # If some prices are flat but not all, use default calculation
        
    rs = up / down
    rsi = np.zeros_like(prices)
    rsi[:period] = 100. - 100. / (1. + rs)

    for i in range(period, len(prices)):
        delta = deltas[i - 1]
        if delta > 0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta

        up = (up * (period - 1) + upval) / period
        down = (down * (period - 1) + downval) / period
        
        # Prevent division by zero
        if down == 0:
            rsi[i] = 100
        else:
            rs = up / down
            rsi[i] = 100. - 100. / (1. + rs)

    return rsi

# Initialize Firebase
cred = credentials.Certificate('firebase/serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': FIREBASE_CONFIG['databaseURL']
})

app = Flask(__name__)

@app.route('/')
def index():
    # Fetch data from Firebase
    ref = db.reference('spy_options_test')
    data = ref.get()
    
    if not data:
        return "No data available from Firebase", 500
        
    # Print data structure for debugging
    print("Data structure:", data)
    
    # Process data for plotting
    try:
        if isinstance(data, dict):
            # Extract timestamps and SPY prices
            timestamps = []
            prices = []
            for entry in data.values():
                if isinstance(entry, dict):
                    timestamps.append(entry['timestamp'])
                    prices.append(float(entry['spyPrice']))
            
            # Sort by timestamp
            sorted_data = sorted(zip(timestamps, prices), key=lambda x: x[0])
            x = [item[0] for item in sorted_data]  # Timestamps
            y = [item[1] for item in sorted_data]  # Prices
    except (ValueError, TypeError) as e:
        return f"Error processing data: {str(e)}", 500
    
    # Calculate RSI
    rsi_values = calculate_rsi(y)
    
    # Create price chart
    price_trace = go.Scatter(
        x=x,
        y=y,
        mode='lines+markers',
        name='SPY Price',
        line=dict(color='royalblue', width=2),
        marker=dict(size=6, color='darkblue')
    )
    
    # Create RSI chart
    rsi_trace = go.Scatter(
        x=x,
        y=rsi_values,
        mode='lines',
        name='RSI',
        line=dict(color='purple', width=2)
    )
    
    # Create subplots
    fig = plotly.subplots.make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.1,
        subplot_titles=('SPY Price', 'Relative Strength Index (RSI)')
    )
    
    # Add traces
    fig.add_trace(price_trace, row=1, col=1)
    fig.add_trace(rsi_trace, row=2, col=1)
    
    # Update layout
    fig.update_layout(
        height=800,
        showlegend=True,
        hovermode='x unified'
    )
    
    # Update y-axes
    fig.update_yaxes(title_text='Price ($)', row=1, col=1)
    fig.update_yaxes(title_text='RSI', row=2, col=1)
    fig.update_xaxes(title_text='Time', row=2, col=1)
    
    graph_json = plotly.io.to_json(fig)
    
    return render_template_string('''
        <html>
            <head>
                <title>Plotly Graph</title>
                <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            </head>
            <body>
                <div id="plotly-graph"></div>
                <script>
                    var graph = {{ graph_json|safe }};
                    Plotly.newPlot('plotly-graph', graph);
                </script>
            </body>
        </html>
    ''', graph_json=graph_json)

if __name__ == '__main__':
    import socket
    from contextlib import closing
    
    def find_free_port(start_port):
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
            port = start_port
            while port < start_port + 100:
                try:
                    s.bind(('', port))
                    return port
                except OSError:
                    port += 1
            raise OSError("No available ports in range")
    
    port = find_free_port(51153)
    print(f"Starting server on port {port}")
    app.run(host='0.0.0.0', port=port)