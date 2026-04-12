import json
import requests
import os
from datetime import datetime, timedelta

def chore_boy_fetch():
    api_key = os.getenv("Rangus_Jangus")
    if not api_key:
        print(">> CHORE BOY ERROR: Rangus_Jangus key not found.")
        return None

    # Get date range for the last 30 days
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    
    # Updated URL to fetch 'aggregates' (historical candles)
    api_url = f"https://api.polygon.io/v2/aggs/ticker/AAPL/range/1/day/{start_date}/{end_date}?adjusted=true&sort=asc&apiKey={api_key}"
    
    try:
        response = requests.get(api_url)
        data = response.json()
        results = data.get("results", [])
        
        if not results:
            return None

        # Logic Layer: Calculate 20-day Simple Moving Average (SMA)
        closes = [day["c"] for day in results]
        current_price = closes[-1]
        sma_20 = sum(closes[-20:]) / 20 if len(closes) >= 20 else sum(closes) / len(closes)
        
        # Simple Technical Analysis Signal
        signal_status = "BULLISH" if current_price > sma_20 else "BEARISH"

        target_variables = {
            "ticker": "AAPL",
            "current_price": current_price,
            "sma_20": round(sma_20, 2),
            "signal": signal_status,
            "timestamp": end_date
        }
        
        print(f">> CHORE BOY: {signal_status} signal secured for {target_variables['ticker']}.")
        return target_variables
        
    except Exception as e:
        print(f">> CHORE BOY ERROR: Logic failure - {e}")
        return None

def deploy_signal():
    market_data = chore_boy_fetch()
    if not market_data:
        return

    veritas_payload = {
        "status": "active",
        "signal": "VERITAS_ALPHA",
        "analysis": market_data
    }

    with open('veritas_data.json', 'w') as f:
        json.dump(veritas_payload, f, indent=4)

    print(">> VERITAS: Technical Analysis Handshake Complete.")

if __name__ == "__main__":
    deploy_signal()
    
