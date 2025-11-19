# Yahoo Finance MCP Server

A Model Context Protocol (MCP) server that provides access to Yahoo Finance data through the RapidAPI Yahoo Finance 15 API. This server offers 24 tools for retrieving stock market data, financial statements, options data, and more.

## Features

- **Stock Market Data**: Real-time quotes, historical data, and market statistics
- **Financial Statements**: Income statements, balance sheets, cash flow statements
- **Earnings Data**: Quarterly earnings, estimates, and historical trends
- **Options Data**: Complete options chains with strikes and premiums
- **Market Analysis**: Insider trading, institutional ownership, analyst recommendations
- **Company Information**: Profiles, key statistics, and calendar events

## Available Tools

### Market Data Tools
1. **search** - Search for stocks, ETFs, and mutual funds
2. **get_market_quotes** - Get current market quotes for stocks
3. **get_market_news** - Fetch market news for specific tickers
4. **get_market_screener** - Get trending stocks and market movers

### Stock Data Tools
5. **get_stock_profile** - Company profile and business information
6. **get_stock_financial_data** - Comprehensive financial metrics and ratios
7. **get_stock_key_statistics** - Key statistics and valuation metrics
8. **get_stock_balance_sheet** - Balance sheet data (quarterly and annual)
9. **get_stock_insider_holders** - Major insider holders information
10. **get_stock_sec_filings** - SEC filings and documents

### Analysis Tools
11. **get_stock_recommendation_trend** - Analyst recommendation trends
12. **get_stock_upgrade_downgrade_history** - Analyst upgrades/downgrades
13. **get_stock_net_share_purchase_activity** - Net share purchase statistics
14. **get_stock_institution_ownership** - Institutional ownership data
15. **get_stock_index_trend** - Index-related trend data
16. **get_stock_insider_transactions** - Insider trading activity
17. **get_stock_cashflow_statement** - Cash flow statement data (quarterly and annual)
18. **get_stock_calendar_events** - Earnings dates, dividends, and events
19. **get_stock_earnings_trend** - Earnings trend analysis
20. **get_stock_earnings_history** - Historical earnings data
21. **get_stock_earnings** - Earnings data and quarterly results
22. **get_stock_income_statement** - Income statement data (quarterly and annual)
23. **get_stock_history** - Historical price data with various intervals

### Options Data
24. **get_options_data** - Complete options chains with strikes and premiums


### Claude Desktop Setup

Add the following to your Claude Desktop configuration file (`claude_desktop_config.json`):

```json
"YahooFinance": {
    "command": "uvx",
    "args": [
        "--from",
        "git+https://github.com/Tilak-Shenoy/mcp-yh-finance.git",
        "yahoofinance"
    ],
    "env": {
        "RAPIDAPI_KEY": "YOUR_API_KEY"
    }
}
```

This should automatically pull the code and run the tools. Follow [Step 4](##4-get-rapidapi-key) to get your API KEY. You can stop here if you are not interested in making any code changes to the server.

## Installation

### Prerequisites
- Python 3.12 or higher
- RapidAPI account with Yahoo Finance 15 API subscription
- MCP-compatible client (e.g., Claude Desktop)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd mcp-yh-finance
   ```

2. **Install dependencies**
   If you don't have `uv` installed, you can install it using the following commands:
   ```bash
   # On macOS and Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # On Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```
  Sync Dependencies
   ```bash
   uv sync
   ```
3. **Set up environment variables**
   Add the following to your Claude Desktop configuration file (`claude_desktop_config.json`):
   ```json
   {
        "mcpServers": {
            "YahooFinance": {
            "command": "uv",
            "args": [
                "--directory",
                "/path/to/mcp-yh-finance",
                "run",
                "yahoofinance"
            ],
            "env": {
                "RAPID_API_KEY": "your_api_key_here"
            }
            }
        }
    }
   ```

4. **Get RapidAPI Key**
   - Sign up at [RapidAPI](https://rapidapi.com/)
   - Subscribe to the [Yahoo Finance 15 API](https://rapidapi.com/sparior/api/yahoo-finance15/)
   - Copy your API key to the env param in the claude_desktop_config.json file

## Tool Parameters

### Common Parameters
- **symbol** (str): Stock ticker symbol (e.g., "AAPL", "GOOGL", "MSFT")
- **interval** (str): Time intervals for historical data
  - Valid values: "1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"
- **date** (str): Date in YYYY-MM-DD format for options and calendar data

### Search Parameters
- **query** (str): Search query for finding stocks/ETFs

### Market Data Parameters
- **tickers** (str): Comma-separated ticker symbols for news
- **type** (str): News type ("ALL", "VIDEO", "PRESS_RELEASE")
- **screener_type** (str): Screener type ("trending", "gainers", "losers", etc.)

## Error Handling

The server provides comprehensive error handling:

- **Invalid parameters**: Returns descriptive error messages
- **API failures**: Returns "Unable to fetch [data]" messages
- **Network issues**: Automatic retry logic (where applicable)
- **Rate limiting**: Respects API rate limits

## API Rate Limits

The Yahoo Finance 15 API has the following is free to use but you can subscibe to get more requests per month and higher rate limits.

Check your RapidAPI dashboard for current usage and limits.

## Development

### Project Structure
```
mcp-yh-finance/
├── src/
│   └── yh_finance/
│       ├── __init__.py
│       ├── main.py          # Server entry point
│       ├── api_handler.py   # API request handler
│       ├── yh_tools.py      # Tool definitions
│       └── .env            # Environment variables
├── pyproject.toml          # Project configuration
└── README.md               # This file
```

### Adding New Tools

1. Define the tool function in `yh_tools.py`
2. Use the `@server.tool()` decorator
3. Follow the naming convention: `get_[data_type]`
4. Implement proper error handling
5. Add comprehensive docstring

Example:
```python
@server.tool()
async def get_custom_data(ctx: Context, symbol: str) -> str:
    """Get custom data for a stock.
    
    Args:
        symbol (str): Stock symbol.
        
    Returns:
        str: JSON string with custom data.
    """
    url = f"{BASE_URL}/endpoint/{symbol}"
    response = await make_api_request(url, {}, ctx)
    if not response:
        return "Unable to fetch custom data."
    return json.dumps(response, indent=4)
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Update documentation
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

- **Issues**: Report bugs and feature requests on GitHub
- **API Support**: Contact RapidAPI for Yahoo Finance API issues
- **Documentation**: Check this README and inline code documentation

## Changelog

### Version 1.0.0
- Initial release with 24 financial tools
- Support for stocks, ETFs, and mutual funds
- Options data and calendar events
- Comprehensive error handling
- Claude Desktop integration

---

**Note**: This server requires an active RapidAPI subscription to the Yahoo Finance 15 API. Some features may be limited based on your subscription tier.
