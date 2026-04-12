def deploy_signal():
    api_key = os.getenv("Rangus_Jangus")
    # THE 3 SCORE LIST
    watch_list = ["AMC", "WBA", "NVDA"]
    results = {}
    total_score = 0
    
    print(f">> DUTCHMAN: Initiating Phase 2 Hunt...")

    for ticker in watch_list:
        analysis = get_veritas_score(ticker, api_key)
        if analysis:
            results[ticker] = analysis
            total_score += analysis['score']
            print(f">> DUTCHMAN: {ticker} Score: {analysis['score']}")
        # 15s breath to keep Polygon happy
        time.sleep(15) 

    # THE COMPREHENSIVE SCORE
    market_health = round(total_score / len(watch_list)) if watch_list else 0
    
    veritas_payload = {
        "phase": "DUTCHMAN_TWO",
        "market_health_score": market_health,
        "assets": results,
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    # CRITICAL: This is the 'Handshake' that saves the file
    with open('veritas_data.json', 'w') as f:
        json.dump(veritas_payload, f, indent=4)
        
    print(f">> VERITAS: Data persisted to trophy room. Global Health: {market_health}")
    
