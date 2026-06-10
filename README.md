# PaisaPathau.com — Rate Scraper v2
### 24 Countries → Nepal (NPR) | Auto-updates every 30 minutes | $0/month

## Countries Covered
🇦🇺 Australia | 🇺🇸 USA | 🇬🇧 UK | 🇨🇦 Canada | 🇳🇿 New Zealand
🇪🇺 Europe | 🇦🇪 UAE | 🇸🇦 Saudi Arabia | 🇶🇦 Qatar | 🇰🇼 Kuwait
🇧🇭 Bahrain | 🇴🇲 Oman | 🇯🇵 Japan | 🇰🇷 South Korea | 🇲🇾 Malaysia
🇸🇬 Singapore | 🇭🇰 Hong Kong | 🇨🇭 Switzerland | 🇸🇪 Sweden | 🇳🇴 Norway
🇩🇰 Denmark | 🇮🇳 India | 🇹🇭 Thailand | 🇮🇱 Israel

## Quick Setup (15 minutes)

### 1. Get your free API key
- Go to https://www.exchangerate-api.com/
- Sign up free → copy your API key

### 2. Upload to GitHub (free)
- Create account at github.com
- New repository → upload all these files

### 3. Add your API key as a secret
- GitHub repo → Settings → Secrets → New secret
- Name: EXCHANGE_RATE_API_KEY
- Value: (paste your key)

### 4. Enable GitHub Actions
- Click the "Actions" tab in your repo
- Enable workflows
- Done! Runs automatically every 30 minutes, forever, FREE.

## Output: data/latest_rates.json
```json
{
  "last_updated": "2026-06-09T10:00:00Z",
  "send_amount": 1000,
  "total_corridors": 24,
  "corridors": [
    {
      "from_currency": "AUD",
      "country": "Australia",
      "flag": "\ud83c\udde6\ud83c\uddfa",
      "mid_market_rate": 88.45,
      "best_provider": "Wise",
      "best_send_rate": 87.92,
      "best_receive_amount": 87270.40,
      "best_fee": 6.50
    }
  ]
}
```

## Use on your WordPress site
1. Upload data/latest_rates.json to your hosting via FTP
2. Access at: https://paisapathau.com/data/latest_rates.json
3. Use this JavaScript to display rates on any page:

```javascript
fetch("https://paisapathau.com/data/latest_rates.json")
  .then(r => r.json())
  .then(data => {
    data.corridors.forEach(corridor => {
      console.log(corridor.flag + " " + corridor.country +
        ": 1 " + corridor.from_currency + " = " +
        corridor.mid_market_rate + " NPR");
    });
  });
```

## Cost: $0/month
- GitHub Actions: FREE (2000 min/month free)
- ExchangeRate-API: FREE (1500 req/month)
- Wise API: FREE
- Hosting data files: FREE (in your GitHub repo)
