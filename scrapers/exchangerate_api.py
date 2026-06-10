"""
PaisaPathau.com — Multi-Country to NPR Rate Fetcher
Covers 20+ sending countries → Nepal (NPR)
Free API: https://www.exchangerate-api.com/ (1500 req/month free)
"""
import requests
from datetime import datetime

API_KEY = "YOUR_FREE_API_KEY_HERE"  # Get free at exchangerate-api.com

# All major countries with Nepali diaspora + their currencies
SENDING_COUNTRIES = {
    "AUD": {"country": "Australia",     "flag": "🇦🇺"},
    "USD": {"country": "USA",           "flag": "🇺🇸"},
    "GBP": {"country": "UK",            "flag": "🇬🇧"},
    "CAD": {"country": "Canada",        "flag": "🇨🇦"},
    "NZD": {"country": "New Zealand",   "flag": "🇳🇿"},
    "EUR": {"country": "Europe",        "flag": "🇪🇺"},
    "AED": {"country": "UAE",           "flag": "🇦🇪"},
    "SAR": {"country": "Saudi Arabia",  "flag": "🇸🇦"},
    "QAR": {"country": "Qatar",         "flag": "🇶🇦"},
    "KWD": {"country": "Kuwait",        "flag": "🇰🇼"},
    "BHD": {"country": "Bahrain",       "flag": "🇧🇭"},
    "OMR": {"country": "Oman",          "flag": "🇴🇲"},
    "JPY": {"country": "Japan",         "flag": "🇯🇵"},
    "KRW": {"country": "South Korea",   "flag": "🇰🇷"},
    "MYR": {"country": "Malaysia",      "flag": "🇲🇾"},
    "SGD": {"country": "Singapore",     "flag": "🇸🇬"},
    "HKD": {"country": "Hong Kong",     "flag": "🇭🇰"},
    "CHF": {"country": "Switzerland",   "flag": "🇨🇭"},
    "SEK": {"country": "Sweden",        "flag": "🇸🇪"},
    "NOK": {"country": "Norway",        "flag": "🇳🇴"},
    "DKK": {"country": "Denmark",       "flag": "🇩🇰"},
    "INR": {"country": "India",         "flag": "🇮🇳"},
    "THB": {"country": "Thailand",      "flag": "🇹🇭"},
    "ISK": {"country": "Iceland",       "flag": "🇮🇸"},
    "ILS": {"country": "Israel",        "flag": "🇮🇱"},
}

def get_rate(from_currency, amount=1000):
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{from_currency}/NPR/{amount}"
    try:
        r = requests.get(url, timeout=10)
        d = r.json()
        if d.get("result") == "success":
            meta = SENDING_COUNTRIES.get(from_currency, {})
            return {
                "from_currency":    from_currency,
                "country":          meta.get("country", ""),
                "flag":             meta.get("flag", ""),
                "to_currency":      "NPR",
                "mid_market_rate":  round(d["conversion_rate"], 4),
                "send_amount":      amount,
                "receive_amount":   round(d["conversion_result"], 2),
                "timestamp":        datetime.utcnow().isoformat() + "Z",
                "status":           "ok",
            }
        return {"from_currency": from_currency, "status": "error",
                "error": d.get("error-type", "unknown")}
    except Exception as e:
        return {"from_currency": from_currency, "status": "error", "error": str(e)}

def fetch_all(amount=1000):
    results = []
    for currency in SENDING_COUNTRIES:
        r = get_rate(currency, amount)
        results.append(r)
        print(f"  {'✅' if r['status']=='ok' else '❌'} {currency} → NPR: {r.get('mid_market_rate','ERROR')}")
    return results
