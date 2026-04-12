import json
import requests
import os

def chore_boy_fetch():
    # THE CHORE BOY: Hunting live market variables
    # Updated to match your specific naming: Rangus_Jangus
    api_key = os.getenv("Rangus_Jangus") 
    
    if not api_key:
        print(">> CHORE BOY ERROR: Rangus_Jangus key not found in environment.")
        return None

    api_url = f"https://api.polygon.io/v2/aggs/ticker/AAPL/prev?adjusted=true&apiKey={api_key}"
    
    try:
        response = requests.get(api_url)
        live_data = response.json()
        
        target_variables = {
            "ticker": live_data["ticker"],
            "closing_price": live_data["results"][0]["c"],
            "trading_volume": live_data["results"][0]["v"]
        }
        print(f">> CHORE BOY: Live Data Secured for {target_variables['ticker']}.")
        return target_variables
    except Exception as e:
        print(f">> CHORE BOY ERROR: The hunt failed - {e}")
        return None

def deploy_signal():
    market_data = chore_boy_fetch()
    
    veritas_payload = {
        "status": "active",
        "signal": "VERITAS_ALPHA",
        "type": "classic_almond_butter",
        "api_owner": "Rangus_Jangus",
        "market_snapshot": market_data
    }

    with open('veritas_data.json', 'w') as f:
        json.dump(veritas_payload, f, indent=4)

    print(">> VERITAS: Signal Handshake Complete.")

if __name__ == "__main__":
    deploy_signal()
    
