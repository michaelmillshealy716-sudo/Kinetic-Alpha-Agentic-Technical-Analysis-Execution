import json
import requests
import os
import time
from datetime import datetime

def get_veritas_score(ticker, api_key):
    """The 'Dutchman' Logic: SMA + RSI = Veritas Score"""
    # 1. Fetch SMA (Simple Moving Average)
    sma_url = f"https://api.polygon.io/v1/indicators/sma/{ticker}?timespan=day&window=20&apiKey={api_key}"
    # 2. Fetch RSI (Relative Strength Index)
    rsi_url = f"https://api.polygon.io/v1/indicators/rsi/{ticker}?timespan=day&window=14&apiKey={api_key}"
    
    try:
        # Get Current Price first for the SMA check
        price_url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/prev?apiKey={api_key}"
        price_data = requests.get(price_url).json()
        current_price = price_data['results'][0]['c']
        
        sma_val = requests.get(sma_url).json()['results']['values'][0]['value']
        rsi_val = requests.get(rsi_url).json()['results']['values'][0]['value']
        
        # SCORING LOGIC (0-100)
        score = 50 # Start at neutral
        if current_price > sma_val: score += 25 # Trend is up
        else: score -= 25 # Trend is down
        
        if rsi_val < 35: score += 25 # Oversold / Value Buy
        elif rsi_val > 65: score -= 25 # Overbought / High Risk
        
        return {
            "price": round(current_price, 2),
            "sma": round(sma_val, 2),
            "rsi": round(rsi_val, 2),
            "score": score,
            "signal": "BULLISH" if score > 50 else "BEARISH" if score < 50 else "NEUTRAL"
        }
    except:
        return None

def deploy_signal():
    api_key = os.getenv("Rangus_Jangus")
    # YOUR 3 SCORE LIST (AMC, WBA, NVDA)
    watch_list = ["AMC", "WBA", "NVDA"]
    results = {}
    total_score = 0
    
    for ticker in watch_list:
        print(f">> CHORE BOY: Running Dutchman Analysis on {ticker}...")
        analysis = get_veritas_score(ticker, api_key)
        if analysis:
            results[ticker] = analysis
            total_score += analysis['score']
        time.sleep(12) # Respecting the 5-calls-per-minute free tier limit

    # THE COMPREHENSIVE SCORE (Global Market Health)
    comprehensive_score = round(total_score / len(watch_list)) if watch_list else 0
    
    veritas_payload = {
        "phase": "DUTCHMAN_TWO",
        "market_health_score": comprehensive_score,
        "assets": results,
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    with open('veritas_data.json', 'w') as f:
        json.dump(veritas_payload, f, indent=4)
    print(f">> VERITAS: Dutchman Phase 2 Complete. Global Score: {comprehensive_score}")

if __name__ == "__main__":
    deploy_signal()
    
