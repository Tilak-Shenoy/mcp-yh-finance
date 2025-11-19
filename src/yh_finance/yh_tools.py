from mcp.server.fastmcp import Context, FastMCP
from .api_handler import make_api_request, paginated_response, BASE_URL
import json

def reg_tools(server: FastMCP):
    """Register all Yahoo Finance API tools with the MCP server."""
    
    @server.tool()
    async def search(ctx: Context, query: str) -> str:
        """Search for any stock, ETF, or mutual fund. First 5 results are returned.
        
        Args:
            query (str): The search query.
            
        Returns:
            str: JSON string with first 5 results.
        """
        
        url = f"{BASE_URL}/v1/markets/search"
        params = {
            "search": query
        }

        search_response = await make_api_request(url, params, ctx)

        if not search_response or not search_response.get("results", []):
            return "Unable to search the ticker for this query."
                
        search_results = search_response.get("results", [])[:5]
        return json.dumps(search_results, indent=4)
    
    # Market Data endpoints
    @server.tool()
    async def get_market_quotes(ctx: Context, symbol: str, instrument_type: str) -> str:
        """Get current market quote data for stocks, ETFs, mutual funds, etc.
        
        Args:
            symbol (str): One stock symbol.
            instrument_type (str): The type of the instrument, STOCKS/ETF/MUTUALFUNDS.
            
        Returns:
            str: JSON string with quote data.
        """
        url = f"{BASE_URL}/v1/markets/quote"
        params = {
            "ticker": symbol,
            "type": instrument_type
        }
        response = await make_api_request(url, params, ctx)
        if not response:
            return "Unable to fetch quote data."
        return json.dumps(response, indent=4)
    
    @server.tool()
    async def get_market_news(ctx: Context, tickers: str, type: str = "ALL") -> str:
        """Get recently published stock news in all sectors.
        
        Args:
            tickers (str): List of stock tickers.
            type (str): Type of news, ALL/VIDEO/PRESS_RELEASE
            
        Returns:
            str: JSON string with market news.
        """
        url = f"{BASE_URL}/v2/markets/news"
        params = {
            "tickers": tickers,
            "type": type
        }
        response = await make_api_request(url, params, ctx)
        if not response or not response.get("items", []):
            return "Unable to fetch market news."
        
        news_items = response.get("items", [])[:5]
        return json.dumps(news_items, indent=4)

    
    @server.tool()
    async def get_market_screener(ctx: Context, type:str) -> str:
        """Get trending stocks in today's market.

        Args:
            type (str): Type of trends to look for. Choose one of the following options
            trending: Trending tickers in today's market
            undervalued_growth_stocks: Stocks with earnings growth
            growth_technology_stocks: Technology stocks with revenue
            day_gainers: Stocks with the highest gains
            day_losers: Stocks with the highest losses
            most_actives: Stocks by intraday trade volume.
            undervalued_large_caps: Undervalued large cap stocks
            aggressive_small_caps: Small-cap stocks with earnings growth.
            small_cap_gainers: Small caps with a 1 day price change of 5.0%
        
        Returns:
            str: JSON string with trending stocks.
        """
        url = f"{BASE_URL}/v1/markets/screener"
        params = {
            "list": type
        }
        response = await make_api_request(url, params, ctx)
        if not response or not response.get("quotes", []):
            return "Unable to fetch trending stocks."
        
        trending_stocks = response.get("quotes", [])[:5]
        return json.dumps(trending_stocks, indent=4)
    
    # Stock Data endpoints
    @server.tool()
    async def get_stock_profile(ctx: Context, symbol: str) -> str:
        """Get stock profile information such as company name, descriptions, website, etc.
        
        Args:
            symbol (str): Stock symbol.
            
        Returns:
            str: JSON string with stock profile.
        """
        url = f"{BASE_URL}/yahoo/qu/quote/{symbol}/asset-profile"
        response = await make_api_request(url, {}, ctx)
        if not response:
            return "Unable to fetch stock profile."
        return json.dumps(response, indent=4)
    
    @server.tool()
    async def get_stock_financial_data(ctx: Context, symbol: str) -> str:
        """Get the financial data of the given stock.
        
        Args:
            symbol (str): Stock symbol.
            
        Returns:
            str: JSON string with financial data.
        """
        url = f"{BASE_URL}/yahoo/qu/quote/{symbol}/financial-data"
        response = await make_api_request(url, {}, ctx)
        if not response:
            return "Unable to fetch financial data."
        return json.dumps(response, indent=4)
    
    @server.tool()
    async def get_stock_key_statistics(ctx: Context, symbol: str) -> str:
        """Get stock key statistics data.
        
        Args:
            symbol (str): Stock symbol.
            
        Returns:
            str: JSON string with key statistics.
        """
        url = f"{BASE_URL}/yahoo/qu/quote/{symbol}/default-key-statistics"
        response = await make_api_request(url, {}, ctx)
        if not response:
            return "Unable to fetch key statistics."
        return json.dumps(response, indent=4)
    
    @server.tool()
    async def get_stock_balance_sheet(ctx: Context, symbol: str) -> str:
        """Get stock balance sheet data.
        
        Args:
            symbol (str): Stock symbol.
            
        Returns:
            str: JSON string with balance sheet data.
        """
        url = f"{BASE_URL}/yahoo/qu/quote/{symbol}/balance-sheet"
        response = await make_api_request(url, {}, ctx)
        if not response:
            return "Unable to fetch balance sheet data."
        return json.dumps(response, indent=4)
    
    @server.tool()
    async def get_stock_insider_holders(ctx: Context, symbol: str) -> str:
        """Get stock insider holders' information.
        
        Args:
            symbol (str): Stock symbol.
            
        Returns:
            str: JSON string with insider holders.
        """
        url = f"{BASE_URL}/yahoo/qu/quote/{symbol}/insider-holders"
        response = await make_api_request(url, {}, ctx)
        if not response:
            return "Unable to fetch insider holders data."
        return json.dumps(response, indent=4)
    
    @server.tool()
    async def get_stock_sec_filings(ctx: Context, symbol: str) -> str:
        """Get stock SEC filings.
        
        Args:
            symbol (str): Stock symbol.
            
        Returns:
            str: JSON string with SEC filings.
        """
        url = f"{BASE_URL}/yahoo/qu/quote/{symbol}/sec-filings"
        response = await make_api_request(url, {}, ctx)
        if not response or not response.get("data", []):
            return "Unable to fetch SEC filings."
        
        filings = response.get("data", {})[:5] if isinstance(response.get("data", []), list) else response.get("data", {})
        return json.dumps(filings, indent=4)
    
    @server.tool()
    async def get_stock_recommendation_trend(ctx: Context, symbol: str) -> str:
        """Get stock recommendations and trends.
        
        Args:
            symbol (str): Stock symbol.
            
        Returns:
            str: JSON string with recommendation trends.
        """
        url = f"{BASE_URL}/yahoo/qu/quote/{symbol}/recommendation-trend"
        response = await make_api_request(url, {}, ctx)
        if not response:
            return "Unable to fetch recommendation trends."
        return json.dumps(response, indent=4)
    
    @server.tool()
    async def get_stock_upgrade_downgrade_history(ctx: Context, symbol: str) -> str:
        """Get stock upgrade and downgrade history.
        
        Args:
            symbol (str): Stock symbol.
            
        Returns:
            str: JSON string with upgrade/downgrade history.
        """
        url = f"{BASE_URL}/yahoo/qu/quote/{symbol}/upgrade-downgrade-history"
        response = await make_api_request(url, {}, ctx)
        if not response or not response.get("history", []):
            return "Unable to fetch upgrade/downgrade history."
        
        history = response.get("history", [])[:5]
        return json.dumps(history, indent=4)
    
    @server.tool()
    async def get_stock_net_share_purchase_activity(ctx: Context, symbol: str) -> str:
        """Get net share purchase activity information for a particular stock.
        
        Args:
            symbol (str): Stock symbol.
            
        Returns:
            str: JSON string with net share purchase activity.
        """
        url = f"{BASE_URL}/yahoo/qu/quote/{symbol}/net-share-purchase-activity"
        response = await make_api_request(url, {}, ctx)
        if not response:
            return "Unable to fetch net share purchase activity."
        return json.dumps(response, indent=4)
    
    @server.tool()
    async def get_stock_institution_ownership(ctx: Context, symbol: str) -> str:
        """Get stock institution ownership.
        
        Args:
            symbol (str): Stock symbol.
            
        Returns:
            str: JSON string with institution ownership.
        """
        url = f"{BASE_URL}/yahoo/qu/quote/{symbol}/institution-ownership"
        response = await make_api_request(url, {}, ctx)
        if not response or not response.get("ownershipList", []):
            return "Unable to fetch institution ownership."
        
        ownership = response.get("ownershipList", [])[:5]
        return json.dumps(ownership, indent=4)
    
    @server.tool()
    async def get_stock_index_trend(ctx: Context, symbol: str) -> str:
        """Get index trend earnings history information for a particular stock.
        
        Args:
            symbol (str): Stock symbol.
            
        Returns:
            str: JSON string with index trend.
        """
        url = f"{BASE_URL}/yahoo/qu/quote/{symbol}/index-trend"
        response = await make_api_request(url, {}, ctx)
        if not response:
            return "Unable to fetch index trend."
        return json.dumps(response, indent=4)
    
    @server.tool()
    async def get_stock_insider_transactions(ctx: Context, symbol: str) -> str:
        """Get stock insider transactions history.
        
        Args:
            symbol (str): Stock symbol.
            
        Returns:
            str: JSON string with insider transactions.
        """
        url = f"{BASE_URL}/yahoo/qu/quote/{symbol}/insider-transactions"
        response = await make_api_request(url, {}, ctx)
        if not response or not response.get("transactions", []):
            return "Unable to fetch insider transactions."
        
        transactions = response.get("transactions", [])[:5]
        return json.dumps(transactions, indent=4)
    
    @server.tool()
    async def get_stock_cashflow_statement(ctx: Context, symbol: str) -> str:
        """Get stock cash flow statements.
        
        Args:
            symbol (str): Stock symbol.
            
        Returns:
            str: JSON string with cash flow statement.
        """
        url = f"{BASE_URL}/yahoo/qu/quote/{symbol}/cashflow-statement"
        response = await make_api_request(url, {}, ctx)
        if not response:
            return "Unable to fetch cash flow statement."
        return json.dumps(response, indent=4)
    
    @server.tool()
    async def get_stock_calendar_events(ctx: Context, symbol: str) -> str:
        """Get stock calendar events.
        
        Args:
            symbol (str): Stock symbol.
            
        Returns:
            str: JSON string with calendar events.
        """
        url = f"{BASE_URL}/yahoo/qu/quote/{symbol}/calendar-events"
        response = await make_api_request(url, {}, ctx)
        if not response:
            return "Unable to fetch calendar events."
        return json.dumps(response, indent=4)
    
    @server.tool()
    async def get_stock_earnings_trend(ctx: Context, symbol: str) -> str:
        """Get earnings trend earnings history information for a particular stock.
        
        Args:
            symbol (str): Stock symbol.
            
        Returns:
            str: JSON string with earnings trend.
        """
        url = f"{BASE_URL}/yahoo/qu/quote/{symbol}/earnings-trend"
        response = await make_api_request(url, {}, ctx)
        if not response or not response.get("trend", []):
            return "Unable to fetch earnings trend."
        
        trend = response.get("trend", [])[:5]
        return json.dumps(trend, indent=4)
    
    @server.tool()
    async def get_stock_earnings_history(ctx: Context, symbol: str) -> str:
        """Get earnings history information for a particular stock.
        
        Args:
            symbol (str): Stock symbol.
            
        Returns:
            str: JSON string with earnings history.
        """
        url = f"{BASE_URL}/yahoo/qu/quote/{symbol}/earnings-history"
        response = await make_api_request(url, {}, ctx)
        if not response or not response.get("history", []):
            return "Unable to fetch earnings history."
        
        history = response.get("history", [])[:5]
        return json.dumps(history, indent=4)
    
    @server.tool()
    async def get_stock_earnings(ctx: Context, symbol: str) -> str:
        """Get earnings information for a particular stock.
        
        Args:
            symbol (str): Stock symbol.
            
        Returns:
            str: JSON string with earnings information.
        """
        url = f"{BASE_URL}/yahoo/qu/quote/{symbol}/earnings"
        response = await make_api_request(url, {}, ctx)
        if not response:
            return "Unable to fetch earnings information."
        return json.dumps(response, indent=4)
    
    @server.tool()
    async def get_stock_income_statement(ctx: Context, symbol: str) -> str:
        """Get stock income statement data.
        
        Args:
            symbol (str): Stock symbol.
            
        Returns:
            str: JSON string with income statement.
        """
        url = f"{BASE_URL}/yahoo/qu/quote/{symbol}/income-statement"
        response = await make_api_request(url, {}, ctx)
        if not response:
            return "Unable to fetch income statement."
        return json.dumps(response, indent=4)
    
    @server.tool()
    async def get_stock_history(ctx: Context, symbol: str, interval: str = "1d") -> str:
        """Get historic data for stocks, ETFs, mutuals funds, etc.
        
        Args:
            symbol (str): Stock symbol.
            interval (str): Time interval (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo).
            
        Returns:
            str: JSON string with historical data.
        """
        if interval not in ["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"]:
            return "Invalid interval. Please use one of the following: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo"
        url = f"{BASE_URL}/yahoo/hi/history/{symbol}/{interval}"
        response = await make_api_request(url, {}, ctx)
        if not response or not response.get("historical", []):
            return "Unable to fetch historical data."
        
        # Limit to first 5 historical data points
        historical_data = response.get("historical", [])[:5]
        return json.dumps(response, indent=4)
    
    # Options data endpoint
    @server.tool()
    async def get_options_data(ctx: Context, symbol: str, date: str) -> str:
        """Get options data for a specific symbol and date.
        
        Args:
            symbol (str): Stock symbol.
            date (str): Expiration date (YYYY-MM-DD format).
            
        Returns:
            str: JSON string with options data.
        """
        url = f"{BASE_URL}/v1/markets/options?ticker={symbol}&date={date}"
        response = await make_api_request(url, {}, ctx)
        if not response:
            return "Unable to fetch options data."
        return json.dumps(response, indent=4)