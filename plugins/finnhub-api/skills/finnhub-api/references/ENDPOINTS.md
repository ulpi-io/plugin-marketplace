# FinnHub API - Complete Endpoint Reference

## Base URL
```
https://finnhub.io/api/v1
```

## Authentication
```bash
# Header (recommended)
X-Finnhub-Token: your_api_key

# Query parameter
?token=your_api_key
```

## Stock Market Data

### GET /quote
Real-time stock quote.
```
Params: symbol (required)
Returns: c (current), d (change), dp (change %), h (high), l (low), o (open), pc (prev close), t (timestamp)
Free: ✅
```

### GET /stock/candle
Historical OHLCV data.
```
Params: symbol, resolution (1,5,15,30,60,D,W,M), from (unix), to (unix)
Returns: c[], h[], l[], o[], v[], t[], s (status)
Free: ⚠️ Limited (some timeframes restricted)
```

### GET /stock/profile2
Company profile.
```
Params: symbol
Returns: country, currency, exchange, finnhubIndustry, ipo, logo, marketCapitalization, name, phone, shareOutstanding, ticker, weburl
Free: ✅
```

### GET /stock/peers
Similar companies.
```
Params: symbol
Returns: [array of tickers]
Free: ✅
```

## Fundamental Data

### GET /stock/metric
Key financial metrics.
```
Params: symbol, metric (all|price|valuation|margin|profitability)
Returns: metric{}, series{}
Free: ✅
```

### GET /stock/financials
Financial statements.
```
Params: symbol, statement (ic|bs|cf), freq (annual|quarterly)
Returns: financials[]
Free: ✅
```

### GET /stock/financials-reported
SEC-reported financials.
```
Params: symbol
Returns: data[]
Free: ✅
```

### GET /stock/earnings
Earnings history.
```
Params: symbol
Returns: [earnings data]
Free: ✅
```

### GET /stock/recommendation
Analyst recommendations.
```
Params: symbol
Returns: [{period, strongBuy, buy, hold, sell, strongSell}]
Free: ✅
```

### GET /stock/price-target
Analyst price targets.
```
Params: symbol
Returns: lastUpdated, targetHigh, targetLow, targetMean, targetMedian
Free: ✅
```

## News & Sentiment

### GET /company-news
Company-specific news.
```
Params: symbol, from (YYYY-MM-DD), to (YYYY-MM-DD)
Returns: [{category, datetime, headline, id, image, source, summary, url}]
Free: ✅
```

### GET /news
General market news.
```
Params: category (general|forex|crypto|merger)
Returns: [news articles]
Free: ✅
```

## Calendar Events

### GET /calendar/earnings
Earnings calendar.
```
Params: from (YYYY-MM-DD), to (YYYY-MM-DD), symbol (optional)
Returns: {earningsCalendar: [{date, epsActual, epsEstimate, hour, quarter, revenueActual, revenueEstimate, symbol, year}]}
Free: ✅
```

### GET /calendar/ipo
IPO calendar.
```
Params: from, to
Returns: {ipoCalendar: []}
Free: ✅
```

### GET /stock/dividend
Dividend history.
```
Params: symbol, from, to
Returns: [{amount, date, payDate, recordDate, symbol}]
Free: ✅
```

### GET /stock/split
Stock split history.
```
Params: symbol, from, to
Returns: [{date, fromFactor, toFactor, symbol}]
Free: ✅
```

## Forex

### GET /forex/rates
Exchange rates.
```
Params: base (default USD)
Returns: {base, quote{}}
Free: ✅
```

### GET /forex/candle
Forex OHLCV data.
```
Params: symbol (e.g., OANDA:EUR_USD), resolution, from, to
Returns: {c[], h[], l[], o[], v[], t[], s}
Free: ✅
```

### GET /forex/exchange
List forex exchanges.
```
Returns: [exchanges]
Free: ✅
```

### GET /forex/symbol
List forex pairs.
```
Params: exchange
Returns: [{symbol, displaySymbol, description}]
Free: ✅
```

## Cryptocurrency

### GET /crypto/candle
Crypto OHLCV data.
```
Params: symbol (e.g., BINANCE:BTCUSDT), resolution, from, to
Returns: {c[], h[], l[], o[], v[], t[], s}
Free: ✅
```

### GET /crypto/exchange
List crypto exchanges.
```
Returns: [exchanges]
Free: ✅
```

### GET /crypto/symbol
List crypto symbols.
```
Params: exchange
Returns: [{symbol, displaySymbol, description}]
Free: ✅
```

## Reference Data

### GET /stock/symbol
Stock symbols list.
```
Params: exchange (default US)
Returns: [{currency, description, displaySymbol, figi, mic, symbol, type}]
Free: ✅
```

### GET /search
Symbol search.
```
Params: q (query)
Returns: {count, result: [{description, displaySymbol, symbol, type}]}
Free: ✅
```

## WebSocket

### URL
```
wss://ws.finnhub.io?token=your_api_key
```

### Subscribe
```json
{"type": "subscribe", "symbol": "AAPL"}
```

### Unsubscribe
```json
{"type": "unsubscribe", "symbol": "AAPL"}
```

### Trade Data
```json
{
  "type": "trade",
  "data": [
    {"s": "AAPL", "p": 150.25, "t": 1234567890, "v": 100}
  ]
}
```

## Premium Endpoints (Paid Only)

### GET /stock/insider-transactions
Insider trading data.

### GET /stock/insider-sentiment
Insider sentiment score.

### GET /stock/ownership
Institutional ownership.

### GET /stock/fund-ownership
Fund ownership.

### GET /stock/etf-sector
ETF sector exposure.

### GET /etf/profile
ETF profile.

### GET /etf/holdings
ETF holdings.

### GET /stock/esg
ESG scores.

### GET /stock/lobbying
Lobbying activities.

### GET /stock/usa-spending
Government spending.

## Rate Limits

| Tier | Calls/Min | Notes |
|------|-----------|-------|
| Free | 60 | US stocks, forex, crypto |
| Paid | 300+ | Per-market pricing |

## Error Codes

| Code | Meaning |
|------|---------|
| 401 | Invalid API key |
| 403 | Premium endpoint / rate limit |
| 429 | Rate limit exceeded |
