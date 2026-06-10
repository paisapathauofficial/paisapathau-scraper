"""
PaisaPathau.com - Wise Send Rate Fetcher (real quote endpoint)
Returns the ACTUAL receive amount Wise shows on its website, including
the real fee, by calling Wise's unauthenticated quote endpoint:
    POST https://api.wise.com/v3/quotes
Falls back to the public comparison endpoint if the quote call fails.
"""
import requests
from datetime import datetime

# Sending currencies we quote into NPR
SUPPORTED = [
    "AUD", "USD", "GBP", "CAD", "NZD", "EUR", "AED", "SAR",
    "QAR", "KWD", "JPY", "SGD", "CHF", "SEK", "NOK", "MYR",
]

QUOTE_URL = "https://api.wise.com/v3/quotes"
COMPARE_URL = "https://api.transferwise.com/v3/comparisons/"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Content-Type": "application/json",
}


def _pick_payment_option(options):
    """Prefer the standard bank transfer option Wise shows by default."""
    if not options:
        return None
    for o in options:
        if not o.get("disabled") and o.get("payIn") == "BANK_TRANSFER":
            return o
    for o in options:
        if not o.get("disabled"):
            return o
    return options[0]


def _from_quote(from_currency, amount):
    """Call the real Wise quote endpoint. Returns dict or None."""
    payload = {
        "sourceCurrency": from_currency,
        "targetCurrency": "NPR",
        "sourceAmount": amount,
    }
    r = requests.post(QUOTE_URL, json=payload, headers=HEADERS, timeout=15)
    d = r.json()
    rate = d.get("rate")
    option = _pick_payment_option(d.get("paymentOptions"))
    if not rate or not option:
        return None
    fee = option.get("fee", {}).get("total")
    receive = option.get("targetAmount")
    if receive is None or fee is None:
        return None
    return {
        "provider": "Wise",
        "from_currency": from_currency,
        "to_currency": "NPR",
        "exchange_rate": round(float(rate), 4),
        "send_amount": amount,
        "fee": round(float(fee), 2),
        "net_send": round(amount - float(fee), 2),
        "receive_amount": round(float(receive), 2),
        "source": "quote",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "status": "ok",
    }


def _from_comparison(from_currency, amount):
    """Fallback: public comparison endpoint. Returns dict or None."""
    params = {
        "sourceCurrency": from_currency,
        "targetCurrency": "NPR",
        "sendAmount": amount,
    }
    r = requests.get(COMPARE_URL, params=params, headers=HEADERS, timeout=15)
    d = r.json()
    providers = d.get("providers", [])
    for p in providers:
        if str(p.get("alias", "")).lower() == "wise" or p.get("name") == "Wise":
            quotes = p.get("quotes", [])
            if not quotes:
                return None
            q = quotes[0]
            rate = q.get("rate")
            fee = q.get("fee")
            receive = q.get("receivedAmount")
            if rate is None or receive is None:
                return None
            return {
                "provider": "Wise",
                "from_currency": from_currency,
                "to_currency": "NPR",
                "exchange_rate": round(float(rate), 4),
                "send_amount": amount,
                "fee": round(float(fee or 0), 2),
                "net_send": round(amount - float(fee or 0), 2),
                "receive_amount": round(float(receive), 2),
                "source": "comparison",
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "status": "ok",
            }
    return None


def get_wise_rate(from_currency, amount=1000):
    try:
        result = _from_quote(from_currency, amount)
        if result:
            return result
        result = _from_comparison(from_currency, amount)
        if result:
            return result
        return {"provider": "Wise", "from_currency": from_currency,
                "status": "error", "error": "no quote returned"}
    except Exception as e:
        return {"provider": "Wise", "from_currency": from_currency,
                "status": "error", "error": str(e)}


def fetch_all(amount=1000):
    results = []
    for c in SUPPORTED:
        r = get_wise_rate(c, amount)
        if r:
            results.append(r)
            mark = "OK" if r.get("status") == "ok" else "XX"
            print(f"  {mark} Wise {c}->NPR: {r.get('exchange_rate', 'ERR')} "
                  f"recv={r.get('receive_amount', 'ERR')}")
    return results
