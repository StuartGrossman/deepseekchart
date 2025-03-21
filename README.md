# SPY Price and RSI Chart Application

This application displays:
- Real-time SPY price data
- Calculated Relative Strength Index (RSI)
- Dual chart visualization with synchronized time axis
- Overbought/oversold indicators

## Features
- Displays real-time SPY options data from Firebase
- Interactive Plotly visualization
- Secure Firebase integration
- Error handling for missing data
- Hosted on port 51153
- Uses Flask for web server functionality
- Includes proper HTML template rendering

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip3 install flask plotly numpy firebase-admin
   ```
3. Set up Firebase:
   - Create a Firebase project at https://console.firebase.google.com/
   - Go to Project Settings > Service Accounts
   - Generate a new private key and download the JSON file
   - Save the JSON file as `firebase/serviceAccountKey.json`
   - Ensure the file has the following permissions:
     ```json
     {
       "type": "service_account",
       "project_id": "your-project-id",
       "private_key_id": "your-private-key-id",
       "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
       "client_email": "your-service-account-email",
       "client_id": "your-client-id",
       "auth_uri": "https://accounts.google.com/o/oauth2/auth",
       "token_uri": "https://oauth2.googleapis.com/token",
       "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
       "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account-email"
     }
     ```
   - Add your Firebase configuration to `firebase/config.py`

## Running the Application

Start the server:
```bash
python3 app.py
```

Access the application at:
http://localhost:51153

## Development

### Testing

The test suite includes comprehensive tests for:
- RSI calculation
  - Verifies RSI values are within 0-100 range
  - Tests flat, increasing, and decreasing price scenarios
  - Validates RSI response to upward/downward momentum
- Data processing
- Chart generation

Run the test suite:
```bash
python3 -m pytest tests/
```

Test coverage includes:
- `tests/test_rsi.py`: Tests for RSI calculation
- `tests/test_data_processing.py`: Tests for data handling
- `tests/test_chart_generation.py`: Tests for visualization

### Code Structure
- `app.py`: Main application file
- `tests/`: Test directory
- `README.md`: This documentation file

## Dependencies
- Flask
- Plotly
- NumPy

## License
MIT License