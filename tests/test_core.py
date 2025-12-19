# tests/test_core.py
import pytest
from src.ml_engine.features import interpret_signals

def test_rsi_signals():
    # Test that RSI > 70 triggers a 'Sell' warning
    metrics = {"rsi": 75, "macd": 0, "macd_signal": 0, "sma_50": 100, "sma_200": 90}
    result = interpret_signals(100.0, metrics)
    assert "RSI: Overbought" in result['signals'][0]

def test_bearish_signal():
    # Test that RSI < 30 triggers a 'Buy' opportunity
    metrics = {"rsi": 25, "macd": 0, "macd_signal": 0, "sma_50": 100, "sma_200": 90}
    result = interpret_signals(100.0, metrics)
    assert "RSI: Oversold" in result['signals'][0]