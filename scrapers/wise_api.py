"""
PaisaPathau.com — Wise Send Rate Fetcher (Official Free API)
Returns actual send rate (slightly lower than mid-market — includes Wise margin)
"""
import requests
from datetime import datetime

WISE_FEES = {
    "AUD": 0.0065, "USD": 0.0065, "GBP": 0.0050, "CAD": 0.0065,
    "NZD": 0.0070, "EUR": 0.0045, "AED": 0.0070, "SAR": 0.0070,
    "QAR": 0.0070, "KWD": 0.0080, "JPY": 0.0080, "SGD": 0.0065,
    "CHF": 0.0055, "SEK": 0.0070, "NOK": 0.0070, "MYR": 0.0090,
}

SUPPORTED = list(WISE_FEES.keys())

def get_wise_rate(from_currency, amount=1000):
    url = f"https://wise.com/rates/live?source={from_currency}&target=NPR"
    headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        rate = r.json().get("value")
        if not rate:
            return None
        fee = round(amount * WISE_FEES.get(from_currency, 0.0075), 2)
        net  = amount - fee
        return {
            "provider":       "Wise",
            "from_currency":  from_currency,
            "to_currency":    "NPR",
            "exchange_rate":  round(float(rate), 4),
            "send_amount":    amount,
            "fee":            fee,
            "net_send":       net,
            "receive_amount": round(float(rate) * net, 2),
            "timestamp":      datetime.utcnow().isoformat() + "Z",
            "status":         "ok",
        }
    except Exception as e:
        return {"provider": "Wise", "from_currency": from_currency,
                "status": "error", "error": str(e)}

def fetch_all(amount=1000):
    results = []
    for c in SUPPORTED:
        r = get_wise_rate(c, amount)
        if r:
            results.append(r)
            print(f"  {'✅' if r['status']=='ok' else '❌'} Wise {c}→NPR: {r.get('exchange_rate','ERR')}")
    return results
