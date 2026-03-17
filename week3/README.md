# OpenWeatherMap MCP Server

This is a local STDIO MCP (Model Context Protocol) server that wraps the [OpenWeatherMap API](https://openweathermap.org/api) to provide weather information tools.

## Features

- Two MCP tools:
  1. `get_current_weather` - Get current weather for any city
  2. `get_forecast` - Get 1-5 day forecast (3-hour intervals)

- Resilience:
  - Graceful error handling for 401 (invalid key), 404 (city not found), 429 (rate limit)
  - Timeout after 10 seconds
  - Logging to stderr (doesn't interfere with STDIO transport)

## Prerequisites

1. Python 3.10+
2. OpenWeatherMap API key (free tier available): https://openweathermap.org/api
3. MCP SDK: `pip install mcp`

## Setup

### 1. Install dependencies

```bash
cd week3
pip install -r requirements.txt
```

**requirements.txt:**
```
mcp>=0.5.0
pydantic>=2.0
httpx>=0.28.0
```

### 2. Configure API key

Set the environment variable before running:
```bash
export OPENWEATHER_API_KEY="your-api-key-here"
```

## Running (Local STDIO)

```bash
cd week3
python server/server.py
```

The server communicates via STDIO - it doesn't listen on any port.

## Configure in Claude Desktop

Add this to your Claude Desktop configuration file:

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "openweather": {
      "command": "python",
      "args": ["/absolute/path/to/modern-software-dev-assignments/week3/server/server.py"],
      "env": {
        "OPENWEATHER_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

## Tool Reference

### `get_current_weather`

**Parameters:**
- `city` (string, required): City name (e.g., "London", "Beijing")
- `country_code` (string, optional): 2-letter country code (e.g., "GB", "CN") to help disambiguate

**Returns:** Formatted text with:
- City and country
- Temperature (°C) and "feels like"
- Weather condition and description
- Humidity, wind speed, pressure, visibility

### `get_forecast`

**Parameters:**
- `city` (string, required): City name
- `country_code` (string, optional): 2-letter country code
- `days` (integer, default: 5, 1-5): Number of days to forecast

**Returns:** Formatted list of forecast intervals (each 3 hours) with temperature and description.

## Error Handling

The server returns human-readable error messages for:
- Missing API key
- Invalid API key (401)
- City not found (404)
- Rate limit exceeded (429)
- Request timeout
- Other network errors

## Evaluation Checklist

- [x] Exposes at least 2 MCP tools ✓
- [x] Graceful error handling ✓
- [x] Rate limit awareness (passes through 429 errors) ✓
- [x] Clear setup instructions ✓
- [x] Local STDIO deployment mode ✓
- [x] Structured parameter definitions using Pydantic ✓
- [x] Correct logging to stderr (no stdout pollution for STDIO transport) ✓
