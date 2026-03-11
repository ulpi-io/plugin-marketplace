#!/usr/bin/env python3
"""
FinnHub API Client - Production-ready wrapper for FinnHub financial data API.

Usage:
    from finnhub_client import FinnHubClient

    client = FinnHubClient()  # Uses FINNHUB_API_KEY env var
    quote = client.get_quote("AAPL")
    profile = client.get_company_profile("AAPL")
"""

import os
import time
import json
import requests
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from functools import wraps


def rate_limit(calls_per_minute: int = 60):
    """Decorator to enforce rate limiting."""
    min_interval = 60.0 / calls_per_minute
    last_called = [0.0]

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)
            last_called[0] = time.time()
            return func(*args, **kwargs)
        return wrapper
    return decorator


class FinnHubClient:
    """Production-ready FinnHub API client with rate limiting and error handling."""

    BASE_URL = "https://finnhub.io/api/v1"

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize FinnHub client.

        Args:
            api_key: FinnHub API key. If not provided, reads from FINNHUB_API_KEY env var.
        """
        self.api_key = api_key or os.getenv("FINNHUB_API_KEY")
        if not self.api_key:
            raise ValueError("API key required. Set FINNHUB_API_KEY or pass api_key parameter.")

        self.session = requests.Session()
        self.session.headers.update({"X-Finnhub-Token": self.api_key})

    @rate_limit(calls_per_minute=60)
    def _request(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Make rate-limited API request with error handling."""
        try:
            response = self.session.get(f"{self.BASE_URL}/{endpoint}", params=params or {})

            # Check rate limit headers
            remaining = response.headers.get("X-Ratelimit-Remaining")
            if remaining and int(remaining) < 5:
                print(f"Warning: Only {remaining} API calls remaining this minute")

            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError as e:
            if response.status_code == 429:
                print("Rate limit exceeded. Waiting 60 seconds...")
                time.sleep(60)
                return self._request(endpoint, params)
            raise Exception(f"HTTP error {response.status_code}: {e}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {e}")

    # ==================== Stock Market Data ====================

    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """
        Get real-time quote for a symbol.

        Returns:
            {
                "c": current_price,
                "d": change,
                "dp": change_percent,
                "h": high,
                "l": low,
                "o": open,
                "pc": previous_close,
                "t": timestamp
            }
        """
        return self._request("quote", {"symbol": symbol})

    def get_candles(
        self,
        symbol: str,
        resolution: str = "D",
        from_time: Optional[int] = None,
        to_time: Optional[int] = None,
        days: int = 30
    ) -> Dict[str, Any]:
        """
        Get historical OHLCV candle data.

        Args:
            symbol: Stock symbol
            resolution: 1, 5, 15, 30, 60, D, W, M
            from_time: Unix timestamp (optional)
            to_time: Unix timestamp (optional)
            days: Number of days if timestamps not provided

        Returns:
            {
                "c": [closes],
                "h": [highs],
                "l": [lows],
                "o": [opens],
                "v": [volumes],
                "t": [timestamps],
                "s": "ok"
            }
        """
        if to_time is None:
            to_time = int(time.time())
        if from_time is None:
            from_time = to_time - (days * 24 * 60 * 60)

        return self._request("stock/candle", {
            "symbol": symbol,
            "resolution": resolution,
            "from": from_time,
            "to": to_time
        })

    def get_company_profile(self, symbol: str) -> Dict[str, Any]:
        """
        Get company profile information.

        Returns:
            {
                "country": "US",
                "currency": "USD",
                "exchange": "NASDAQ",
                "finnhubIndustry": "Technology",
                "ipo": "1980-12-12",
                "logo": "url",
                "marketCapitalization": 2500000,
                "name": "Apple Inc",
                "phone": "123-456-7890",
                "shareOutstanding": 16000,
                "ticker": "AAPL",
                "weburl": "https://apple.com"
            }
        """
        return self._request("stock/profile2", {"symbol": symbol})

    def get_peers(self, symbol: str) -> List[str]:
        """Get list of similar companies."""
        return self._request("stock/peers", {"symbol": symbol})

    # ==================== Fundamental Data ====================

    def get_basic_financials(self, symbol: str, metric: str = "all") -> Dict[str, Any]:
        """
        Get key financial metrics.

        Args:
            symbol: Stock symbol
            metric: "all", "price", "valuation", "margin", "profitability"
        """
        return self._request("stock/metric", {"symbol": symbol, "metric": metric})

    def get_financials(
        self,
        symbol: str,
        statement: str = "ic",
        freq: str = "annual"
    ) -> Dict[str, Any]:
        """
        Get financial statements.

        Args:
            symbol: Stock symbol
            statement: "ic" (income), "bs" (balance sheet), "cf" (cash flow)
            freq: "annual" or "quarterly"
        """
        return self._request("stock/financials", {
            "symbol": symbol,
            "statement": statement,
            "freq": freq
        })

    def get_earnings(self, symbol: str) -> Dict[str, Any]:
        """Get historical earnings data."""
        return self._request("stock/earnings", {"symbol": symbol})

    def get_recommendations(self, symbol: str) -> List[Dict[str, Any]]:
        """Get analyst recommendations."""
        return self._request("stock/recommendation", {"symbol": symbol})

    def get_price_target(self, symbol: str) -> Dict[str, Any]:
        """Get analyst price targets."""
        return self._request("stock/price-target", {"symbol": symbol})

    # ==================== News & Sentiment ====================

    def get_company_news(
        self,
        symbol: str,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        days: int = 7
    ) -> List[Dict[str, Any]]:
        """
        Get company news.

        Args:
            symbol: Stock symbol
            from_date: YYYY-MM-DD format
            to_date: YYYY-MM-DD format
            days: Days of news if dates not provided
        """
        if to_date is None:
            to_date = datetime.now().strftime("%Y-%m-%d")
        if from_date is None:
            from_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

        return self._request("company-news", {
            "symbol": symbol,
            "from": from_date,
            "to": to_date
        })

    def get_market_news(self, category: str = "general") -> List[Dict[str, Any]]:
        """
        Get general market news.

        Args:
            category: "general", "forex", "crypto", "merger"
        """
        return self._request("news", {"category": category})

    # ==================== Calendar Events ====================

    def get_earnings_calendar(
        self,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        symbol: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get upcoming earnings announcements."""
        params = {}
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date
        if symbol:
            params["symbol"] = symbol

        return self._request("calendar/earnings", params)

    def get_ipo_calendar(
        self,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get upcoming IPOs."""
        params = {}
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date

        return self._request("calendar/ipo", params)

    def get_dividends(
        self,
        symbol: str,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get dividend history."""
        params = {"symbol": symbol}
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date

        return self._request("stock/dividend", params)

    # ==================== Forex & Crypto ====================

    def get_forex_rates(self, base: str = "USD") -> Dict[str, Any]:
        """Get forex exchange rates."""
        return self._request("forex/rates", {"base": base})

    def get_forex_candles(
        self,
        symbol: str,
        resolution: str = "D",
        from_time: Optional[int] = None,
        to_time: Optional[int] = None,
        days: int = 30
    ) -> Dict[str, Any]:
        """Get forex OHLCV data."""
        if to_time is None:
            to_time = int(time.time())
        if from_time is None:
            from_time = to_time - (days * 24 * 60 * 60)

        return self._request("forex/candle", {
            "symbol": symbol,
            "resolution": resolution,
            "from": from_time,
            "to": to_time
        })

    def get_crypto_candles(
        self,
        symbol: str,
        resolution: str = "D",
        from_time: Optional[int] = None,
        to_time: Optional[int] = None,
        days: int = 30
    ) -> Dict[str, Any]:
        """Get crypto OHLCV data."""
        if to_time is None:
            to_time = int(time.time())
        if from_time is None:
            from_time = to_time - (days * 24 * 60 * 60)

        return self._request("crypto/candle", {
            "symbol": symbol,
            "resolution": resolution,
            "from": from_time,
            "to": to_time
        })

    def get_crypto_exchanges(self) -> List[str]:
        """Get list of supported crypto exchanges."""
        return self._request("crypto/exchange")

    # ==================== Utility Methods ====================

    def get_stock_symbols(self, exchange: str = "US") -> List[Dict[str, Any]]:
        """Get all stock symbols for an exchange."""
        return self._request("stock/symbol", {"exchange": exchange})

    def search_symbol(self, query: str) -> Dict[str, Any]:
        """Search for symbols by name or ticker."""
        return self._request("search", {"q": query})


# ==================== Quick Test ====================

def test_client():
    """Test the FinnHub client with basic operations."""
    print("Testing FinnHub Client...")
    print("=" * 50)

    try:
        client = FinnHubClient()

        # Test quote
        print("\n1. Testing get_quote('AAPL')...")
        quote = client.get_quote("AAPL")
        print(f"   AAPL: ${quote['c']:.2f} ({quote['dp']:+.2f}%)")

        # Test profile
        print("\n2. Testing get_company_profile('AAPL')...")
        profile = client.get_company_profile("AAPL")
        print(f"   {profile['name']} - {profile['finnhubIndustry']}")
        print(f"   Market Cap: ${profile['marketCapitalization']:,.0f}M")

        # Test candles
        print("\n3. Testing get_candles('AAPL', days=5)...")
        candles = client.get_candles("AAPL", days=5)
        if candles.get("s") == "ok":
            print(f"   Got {len(candles['c'])} candles")
            print(f"   Latest close: ${candles['c'][-1]:.2f}")

        # Test news
        print("\n4. Testing get_company_news('AAPL', days=3)...")
        news = client.get_company_news("AAPL", days=3)
        print(f"   Found {len(news)} news articles")
        if news:
            print(f"   Latest: {news[0].get('headline', 'N/A')[:60]}...")

        # Test financials
        print("\n5. Testing get_basic_financials('AAPL')...")
        financials = client.get_basic_financials("AAPL")
        metrics = financials.get("metric", {})
        print(f"   P/E Ratio: {metrics.get('peBasicExclExtraTTM', 'N/A')}")
        print(f"   ROE: {metrics.get('roeTTM', 'N/A')}")

        print("\n" + "=" * 50)
        print("All tests passed!")
        return True

    except Exception as e:
        print(f"\nError: {e}")
        return False


if __name__ == "__main__":
    test_client()
