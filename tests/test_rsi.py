import numpy as np
from app import calculate_rsi

def test_rsi_calculation():
    # Test data - prices with clear upward and downward movements
    prices = np.array([44, 44.15, 44.09, 44.15, 44.41, 44.46, 44.50, 
                      44.48, 44.55, 44.60, 44.65, 44.70, 44.75, 44.80,
                      44.85, 44.90, 44.95, 45.00, 45.05, 45.10])
    
    # Calculate RSI
    rsi = calculate_rsi(prices)
    
    # Verify RSI values are within expected range
    assert np.all(rsi >= 0) and np.all(rsi <= 100)
    
    # Verify RSI increases with upward momentum
    assert np.all(np.diff(rsi[14:]) >= 0)  # After initial period
    
    # Test edge cases
    # Flat prices should result in RSI = 50
    flat_prices = np.array([100] * 20)
    flat_rsi = calculate_rsi(flat_prices)
    assert np.all(flat_rsi[14:] == 50)
    
    # Strictly increasing prices should result in RSI = 100
    increasing_prices = np.arange(100, 120)
    increasing_rsi = calculate_rsi(increasing_prices)
    assert np.all(increasing_rsi[14:] == 100)
    
    # Strictly decreasing prices should result in RSI = 0
    decreasing_prices = np.arange(120, 100, -1)
    decreasing_rsi = calculate_rsi(decreasing_prices)
    assert np.all(decreasing_rsi[14:] == 0)