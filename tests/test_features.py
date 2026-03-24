import pytest
import pandas as pd
import numpy as np
import sys
import os

# Ensure the src module can be found
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.ml_engine.features import add_technical_indicators

def test_add_technical_indicators():
    """Tests if the feature engineering pipeline successfully calculates all required metrics."""
    
    # 1. Create a dummy dataframe mimicking Yahoo Finance 1-year historical data
    dates = pd.date_range(start='2025-01-01', periods=250, freq='B')
    df = pd.DataFrame({
        'Open': np.random.uniform(100, 150, 250),
        'High': np.random.uniform(110, 160, 250),
        'Low': np.random.uniform(90, 140, 250),
        'Close': np.random.uniform(100, 150, 250),
        'Volume': np.random.randint(1000, 10000, 250)
    }, index=dates)
    
    # 2. Run the function
    result_df = add_technical_indicators(df)
    
    # 3. Assert the expected columns were created for the XGBoost model
    expected_columns = ['rsi', 'macd', 'macd_signal', 'sma_50', 'sma_200', 'atr']
    for col in expected_columns:
        assert col in result_df.columns, f"Failure: Missing engineered feature: {col}"
        
    # 4. Assert the data wasn't destroyed in the process
    assert len(result_df) > 0, "Failure: The dataframe became empty after processing."