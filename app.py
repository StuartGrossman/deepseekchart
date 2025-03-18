from flask import Flask, render_template_string
import plotly.graph_objs as go
import plotly
import firebase_admin
from firebase_admin import credentials, db
from firebase.config import FIREBASE_CONFIG

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
    
    # Create chart from Firebase data
    trace = go.Scatter(
        x=x,
        y=y,
        mode='lines+markers',
        name='SPY Price',
        line=dict(color='royalblue', width=2),
        marker=dict(size=6, color='darkblue')
    )
    
    layout = go.Layout(
        title='SPY Price Over Time',
        xaxis={'title': 'Time', 'type': 'date'},
        yaxis={'title': 'Price ($)'},
        hovermode='x unified'
    )
    
    fig = go.Figure(data=[trace], layout=layout)
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