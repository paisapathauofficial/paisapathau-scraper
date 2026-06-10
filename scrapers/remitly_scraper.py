"""
PaisaPathau.com — Remitly Rate Scraper
Corridors: AUD, USD, GBP, CAD, NZD, EUR, AED → NPR
"""
import requests
from datetime import datetime

CORRIDORS = [
    ("AUD", "AU"), ("USD", "US"), ("GBP", "GB"),
    ("CAD", "CA"), ("NZD", "NZ"), ("EUR", "DE"),
    ("AED", "AE"),
]

def get_remitly_rate(from_currency, from_country, amount=1000):
    url = "https://api.remitly.io/v3/pricing/rates"
    params = {
        "conduit_id":   f"{from_country.upper()}NPL:{from_currency}NPR",
        "input_amount": amount,
        "input_type":   "sending_amount",
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept":     "application/json",
        "Origin":     "https://www.remitly.com",
        "Referer":    "https://www.remitly.com/",
    }
    try:
        r = requests.get(url, params=params, headers=headers, timeout=15)
        d = r.json()
        rate = float(d.get("rate", {}).get("exchange_rate", 0))
        fee  = float(d.get("fee",  {}).get("base_fee", 0))
        if rate:
            return {
                "provider":       "Remitly",
                "from_currency":  from_currency,
                "to_currency":    "NPR",
                "exchange_rate":  round(rate, 4),
                "send_amount":    amount,
                "fee":            fee,
                "receive_amount": round(rate * (amount - fee), 2),
                "timestamp":      datetime.utcnow().isoformat() + "Z",
                "status":         "ok",
            }
        return {"provider": "Remitly", "from_currency": from_currency,
                "status": "error", "error": "no rate", "raw": str(d)[:100]}
    except Exception as e:
        return {"provider": "Remitly", "from_currency": from_currency,
                "status": "error", "error": str(e)}

def fetch_all(amount=1000):
    results = [get_remitly_rate(c, cc, amount) for c, cc in CORRIDORS]
    for r in results:
        print(f"  {'✅' if r['status']=='ok' else '❌'} Remitly {r['from_currency']}→NPR: {r.get('exchange_rate','ERR')}")
    return results
