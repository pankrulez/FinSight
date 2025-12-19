import pandas as pd
import ta
from ta.momentum import RSIIndicator
from ta.trend import SMAIndicator, MACD
from ta.volatility import BollingerBands, AverageTrueRange

def add_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Adds RSI, MACD, and SMAs to the dataframe."""
    if df.empty: return df
    
    df = df.copy() # Avoid SettingWithCopy warnings
    
    # 1. Trend & Momentum
    df['rsi'] = RSIIndicator(close=df['Close'], window=14).rsi()
    macd = MACD(close=df['Close'])
    df['macd'] = macd.macd()
    df['macd_signal'] = macd.macd_signal()
    df['sma_50'] = SMAIndicator(close=df['Close'], window=50).sma_indicator()
    df['sma_200'] = SMAIndicator(close=df['Close'], window=200).sma_indicator()
    
    # 2. Volatility
    bb = BollingerBands(close=df['Close'], window=20, window_dev=2)
    df['bb_high'] = bb.bollinger_hband()
    df['bb_low'] = bb.bollinger_lband()
    df['atr'] = AverageTrueRange(high=df['High'], low=df['Low'], close=df['Close']).average_true_range()
    
    df.dropna(inplace=True)
    return df

def interpret_signals(current_price: float, indicators: dict) -> dict:
    """Translates numbers into text signals."""
    signals = []
    
    # RSI
    if indicators['rsi'] > 70: signals.append("RSI: Overbought (Sell Risk)")
    elif indicators['rsi'] < 30: signals.append("RSI: Oversold (Buy Opp)")
    
    # MACD
    if indicators['macd'] > indicators['macd_signal']: signals.append("MACD: Bullish Crossover")
    else: signals.append("MACD: Bearish Trend")
    
    # SMA
    if indicators['sma_50'] > indicators['sma_200']: signals.append("Golden Cross (Long-term Bullish)")
    elif indicators['sma_50'] < indicators['sma_200']: signals.append("Death Cross (Long-term Bearish)")
    
    return {"signals": signals}