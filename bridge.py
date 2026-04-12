import json
import requests
import os
import time
from datetime import datetime

def get_veritas_score(ticker, api_key):
    try:
        # Price
        p_url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/prev?apiKey={api_key}"
        price = requests.get(p_url).json()['results'][0]['c']
        time.sleep(13) # Aggressive breath for rate limit

        # SMA
        s_url = f"https://api.polygon.io/v1/indicators/sma/{ticker}?timespan=day&window=20&apiKey={api_key}"
        sma_resp = requests.get(s_url).json()
        sma = sma_resp['results']['values'][0]['value']
        time.sleep(13)

        # RSI
        r_url = f"https://api.polygon.io/v1/indicators/rsi/{ticker}?timespan=day&window=14&apiKey={api_key}"
        rsi_resp = requests.get(r_url).json()
        rsi = rsi_resp['results']['values'][0]['value']
        
        score = 50
        if price > sma: score += 25
        else: score -= 25
        if rsi < 35: score += 25
        elif rsi > 65: score -= 25
        
        return {"price": price, "sma": sma, "rsi": rsi, "score": score}
    except Exception as e:
        print(f"Skipping {ticker} due to: {e}")
        return None

def deploy_signal():
    api_key = os.getenv("Rangus_Jangus")
    watch_list = ["AMC", "WBA", "NVDA"]
    results = {}
    
    for ticker in watch_list:
        data = get_veritas_score(ticker, api_key)
        if data:
            results[ticker] = data
        time.sleep(1) # Final buffer

    payload = {
        "phase": "DUTCHMAN_TWO",
        "market_snapshot": results,
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    with open('veritas_data.json', 'w') as f:
        json.dump(payload, f, indent=4)

if __name__ == "__main__":
    deploy_signal()
    
