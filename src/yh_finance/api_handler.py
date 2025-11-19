
from mcp.server.fastmcp import Context
from typing import Optional, Dict, Any
import os
import requests

BASE_URL = "https://yahoo-finance15.p.rapidapi.com/api"

async def make_api_request(url: str, querystring: dict[str, Any], ctx: Optional[Context] = None) -> Optional[Dict[str, Any]]:
    """ Make a request to the API and return the response. """
    api_key = None
    if ctx and hasattr(ctx, 'session_config') and ctx.session_config:
        api_key = ctx.session_config.rapidAPIKey
    
    if not api_key:
        api_key = os.getenv("RAPIDAPI_KEY")
    
    # Not in cache, make the request
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "yahoo-finance15.p.rapidapi.com",
    }
    
    if not api_key:
        raise ValueError("API key not found. Please set the RAPIDAPI_KEY environment variable or provide rapidAPIKey in the request.")
    
    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=30.0)
        response.raise_for_status()
        data = response.json()
        
        # Cache the response
        # cache_manager.cache.set(cache_key, data)
            
        return data
    except Exception as e:
        raise ValueError(f"Unable to fetch data from Yahoo Finance. Please try again later. Error: {e}")

def paginated_response(items, start, total_count=None):
    """Format a paginated response with a fixed page size of 5."""
    if total_count is None:
        total_count = len(items)
    
    # Validate starting index
    start = max(0, min(total_count - 1 if total_count > 0 else 0, start))
    
    # Fixed page size of 5
    page_size = 5
    end = min(start + page_size, total_count)
    
    return {
        "items": items[start:end],
        "start": start,
        "count": end - start,
        "totalCount": total_count,
        "hasMore": end < total_count,
        "nextStart": end if end < total_count else None
    }