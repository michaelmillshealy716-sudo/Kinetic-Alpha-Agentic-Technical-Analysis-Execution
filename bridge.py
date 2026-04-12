import json
import requests
import os
import time
from datetime import datetime

def get_veritas_score(ticker, api_key):
    try:
        # 1. Price Hunt
        price_url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/prev?apiKey={api_key}"
        price_data = requests.get(price_url).json()
        current_price = price_data['results'][0]['c']
        time.sleep(15) # The "Breath"

        # 2. SMA Hunt
        sma_url = f"https://api.polygon.io/v1/indicators/sma/{ticker}?timespan=day&window=20&apiKey={api_key}"
        sma_val = requests.get(sma_url).json()['results']['values'][0]['value']
        time.sleep(15) # The "Breath"

        # 3. RSI Hunt
        rsi_url = f"https://api.polygon.io/v1/indicators/rsi/{ticker}?timespan=day&window=14&apiKey={api_key}"
        rsi_val = requests.get(rsi_url).json()['results']['values'][0]['value']
        time.sleep(15) # The "Breath"
        
        # Confluence Calculus
        score = 50
        if current_price > sma_val: score += 25
        else: score -= 25
        
        if rsi_val < 35: score += 25
        elif rsi_val > 65: score -= 25
        
        return {
            "price": round(current_price, 2),
            "sma": round(sma_val, 2),
            "rsi": round(rsi_val, 2),
            "score": score,
            "signal": "BULLISH" if score > 50 else "BEARISH" if score < 50 else "NEUTRAL"
        }
    except Exception as e:
        print(f">> CHORE BOY: Failed on {ticker}: {e}")
        return None

# ... rest of deploy_signal() stays the same ...

