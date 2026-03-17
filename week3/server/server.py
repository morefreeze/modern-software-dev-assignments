#!/usr/bin/env python3
"""
MCP Server for OpenWeatherMap API
Provides weather query tools via Model Context Protocol
"""

import os
import asyncio
import httpx
from typing import Any, Dict, List, Optional
from mcp.server import Server
from mcp.server.stdio import stdio_server
from pydantic import BaseModel, Field
import logging

# Configure logging to stderr (doesn't interfere with STDIO transport)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=logging.stderr
)
logger = logging.getLogger(__name__)

API_BASE_URL = "https://api.openweathermap.org/data/2.5"
DEFAULT_TIMEOUT = 10.0  # seconds

class WeatherClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = httpx.AsyncClient(timeout=DEFAULT_TIMEOUT)

    async def get_current_weather(self, city: str, country_code: Optional[str] = None) -> Dict[str, Any]:
        """Get current weather for a city."""
        q = city
        if country_code:
            q = f"{city},{country_code}"

        url = f"{API_BASE_URL}/weather"
        params = {
            "q": q,
            "appid": self.api_key,
            "units": "metric"
        }

        response = await self.client.get(url, params=params)
        response.raise_for_status()
        return response.json()

    async def get_forecast(self, city: str, country_code: Optional[str] = None, days: int = 5) -> Dict[str, Any]:
        """Get 5-day forecast for a city."""
        q = city
        if country_code:
            q = f"{city},{country_code}"

        url = f"{API_BASE_URL}/forecast"
        params = {
            "q": q,
            "appid": self.api_key,
            "units": "metric",
            "cnt": days * 8  # 3-hour intervals
        }

        response = await self.client.get(url, params=params)
        response.raise_for_status()
        return response.json()

    async def close(self):
        await self.client.aclose()

# Pydantic models for tool parameters
class GetCurrentWeatherParams(BaseModel):
    city: str = Field(..., description="City name (e.g., London, Beijing)")
    country_code: Optional[str] = Field(None, description="Optional 2-letter country code for better disambiguation")

class GetForecastParams(BaseModel):
    city: str = Field(..., description="City name")
    country_code: Optional[str] = Field(None, description="Optional 2-letter country code")
    days: int = Field(5, description="Number of days to forecast (max 5)", ge=1, le=5)

server = Server("openweather-mcp")

@server.list_tools()
async def list_tools() -> List[Dict[str, Any]]:
    return [
        {
            "name": "get_current_weather",
            "description": "Get current weather information for a city",
            "inputSchema": GetCurrentWeatherParams.model_json_schema()
        },
        {
            "name": "get_forecast",
            "description": "Get multi-day weather forecast for a city (max 5 days)",
            "inputSchema": GetForecastParams.model_json_schema()
        }
    ]

@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
    api_key = os.environ.get("OPENWEATHER_API_KEY")
    if not api_key:
        return [{
            "type": "text",
            "text": "Error: OPENWEATHER_API_KEY environment variable is not set. "
                    "Please get a free API key from https://openweathermap.org/api and set it."
        }]

    client = WeatherClient(api_key)
    try:
        if name == "get_current_weather":
            params = GetCurrentWeatherParams(**arguments)
            data = await client.get_current_weather(params.city, params.country_code)

            # Format the response nicely
            result = (
                f"City: {data['name']}, {data['sys']['country']}\n"
                f"Temperature: {data['main']['temp']}°C (feels like {data['main']['feels_like']}°C)\n"
                f"Weather: {data['weather'][0]['main']} - {data['weather'][0]['description']}\n"
                f"Humidity: {data['main']['humidity']}%\n"
                f"Wind speed: {data['wind']['speed']} m/s\n"
                f"Pressure: {data['main']['pressure']} hPa\n"
                f"Visibility: {data['visibility']} meters\n"
            )
            return [{"type": "text", "text": result}]

        elif name == "get_forecast":
            params = GetForecastParams(**arguments)
            data = await client.get_forecast(params.city, params.country_code, params.days)

            city_name = data['city']['name']
            country = data['city']['country']
            forecast_lines = [f"Forecast for {city_name}, {country} ({len(data['list'])} intervals):"]

            for item in data['list']:
                dt = item['dt_txt']
                temp = item['main']['temp']
                desc = item['weather'][0]['description']
                forecast_lines.append(f"- {dt}: {temp}°C, {desc}")

            return [{"type": "text", "text": "\n".join(forecast_lines)}]

        else:
            return [{"type": "text", "text": f"Error: Unknown tool '{name}'"}]

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            msg = "Error: Invalid API key. Please check your OPENWEATHER_API_KEY."
        elif e.response.status_code == 404:
            msg = f"Error: City not found: {arguments.get('city', 'unknown')}"
        elif e.response.status_code == 429:
            msg = "Error: Rate limit exceeded. OpenWeatherMap API rate limit reached, please try again later."
        else:
            msg = f"HTTP error {e.response.status_code}: {e.response.text}"
        return [{"type": "text", "text": msg}]

    except httpx.TimeoutException:
        return [{"type": "text", "text": "Error: Request timed out connecting to OpenWeatherMap API"}]

    except Exception as e:
        logger.exception("Unexpected error")
        return [{"type": "text", "text": f"Error: {str(e)}"}]

    finally:
        await client.close()

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
