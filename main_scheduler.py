"""
PaisaPathau.com — Main Rate Scheduler
Fetches ALL country → NPR rates every 30 minutes
Saves: data/latest_rates.json + data/latest_rates.csv
Deploy FREE on: Railway.app / Render.com / GitHub Actions
"""
import schedule, time, json, csv, os, argparse
from datetime import datetime
from scrapers.exchangerate_api import fetch_all as mid_rates, SENDING_COUNTRIES
from scrapers.wise_api import fetch_all as wise_rates
from scrapers.remitly_scraper import fetch_all as remitly_rates

OUTPUT = "data"
os.makedirs(OUTPUT, exist_ok=True)

SEND_AMOUNT = 1000  # Default comparison amount

def fetch_and_save():
    print(f"\n{'='*55}")
    print(f"  PaisaPathau Rate Fetch — {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"{'='*55}")

    all_rates   = []
    mid_market  = {}

    # 1. Mid-market rates for ALL 24 currencies
    print("\n[1/3] Mid-market rates (24 countries)...")
    for r in mid_rates(SEND_AMOUNT):
        if r and r.get("status") == "ok":
            mid_market[r["from_currency"]] = r
            all_rates.append({**r, "provider": "Mid-Market (Reference)"})

    # 2. Wise send rates
    print("\n[2/3] Wise send rates...")
    for r in wise_rates(SEND_AMOUNT):
        if r and r.get("status") == "ok":
            all_rates.append(r)

    # 3. Remitly send rates
    print("\n[3/3] Remitly send rates...")
    for r in remitly_rates(SEND_AMOUNT):
        if r and r.get("status") == "ok":
            all_rates.append(r)

    # Build summary — best rate per corridor
    summary = {}
    for r in all_rates:
        cur = r["from_currency"]
        if r.get("provider") == "Mid-Market (Reference)":
            continue
        if cur not in summary or r.get("receive_amount", 0) > summary[cur].get("receive_amount", 0):
            summary[cur] = r

    timestamp = datetime.utcnow().isoformat() + "Z"

    # Build corridor list (all 24 countries with best available rate)
    corridors = []
    for currency, meta in SENDING_COUNTRIES.items():
        mm   = mid_market.get(currency, {})
        best = summary.get(currency, {})
        corridors.append({
            "from_currency":         currency,
            "country":               meta["country"],
            "flag":                  meta["flag"],
            "to_currency":           "NPR",
            "mid_market_rate":       mm.get("mid_market_rate", "N/A"),
            "mid_market_receive":    mm.get("receive_amount", "N/A"),
            "best_provider":         best.get("provider", "N/A"),
            "best_send_rate":        best.get("exchange_rate", "N/A"),
            "best_receive_amount":   best.get("receive_amount", "N/A"),
            "best_fee":              best.get("fee", "N/A"),
            "send_amount":           SEND_AMOUNT,
            "last_updated":          timestamp,
        })

    output = {
        "last_updated":    timestamp,
        "send_amount":     SEND_AMOUNT,
        "send_currency":   "various → NPR",
        "total_corridors": len(corridors),
        "corridors":       corridors,
        "all_rates":       all_rates,
    }

    # Save JSON
    json_path = os.path.join(OUTPUT, "latest_rates.json")
    with open(json_path, "w") as f:
        json.dump(output, f, indent=2)

    # Save history snapshot
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M")
    with open(os.path.join(OUTPUT, f"rates_{ts}.json"), "w") as f:
        json.dump(output, f, indent=2)

    # Save CSV
    csv_path = os.path.join(OUTPUT, "latest_rates.csv")
    if corridors:
        with open(csv_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=corridors[0].keys())
            writer.writeheader()
            writer.writerows(corridors)

    print(f"\n✅ Done! {len(corridors)} corridors | {len(all_rates)} rate records")
    print(f"💾 {json_path}  |  {csv_path}")

    return output


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--once", action="store_true",
                        help="Run once and exit (for GitHub Actions)")
    args = parser.parse_args()

    if args.once:
        fetch_and_save()
        return

    print("PaisaPathau Rate Scheduler — running every 30 minutes")
    fetch_and_save()  # Run immediately
    schedule.every(30).minutes.do(fetch_and_save)
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    main()
