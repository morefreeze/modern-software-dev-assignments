# Week 3 Custom MCP Server - OpenWeatherMap API

## Project Overview
This MCP server wraps the OpenWeatherMap API to provide weather forecast functionality as MCP tools. It exposes two main tools:
1. Get current weather conditions for a city
2. Get 5-day weather forecast for a city

## External API Details
- **API Provider**: OpenWeatherMap (https://openweathermap.org/)
- **Endpoints Used**:
  - Current Weather: `/data/2.5/weather` (GET)
  - 5-Day Forecast: `/data/2.5/forecast` (GET)
- **API Documentation**: https://openweathermap.org/api
- **Rate Limits**: 60 calls/minute (free tier), 1,000,000 calls/day

## MCP Server Architecture
- **Transport**: HTTP (remote deployment mode)
- **Framework**: FastAPI (Python)
- **Port**: 8000 (configurable via environment variable)
- **Resilience**: Timeouts (10 sec), retries (2 attempts), rate limit awareness
- **Authentication**: API key authentication via environment variable

## Files to Create
- `week3/server/main.py` - Main MCP server implementation with FastAPI
- `week3/server/requirements.txt` - Python dependencies
- `week3/README.md` - Setup instructions and tool reference
- `week3/plan.md` - Project plan and tasks (this file)

## Tasks
- [x] Set up week3/server directory structure
- [x] Write plan.md documenting project details
- [x] Implement MCP server with OpenWeatherMap API integration
- [x] Create requirements.txt with dependencies
- [x] Write README.md with setup instructions and tool reference
- [x] Test server locally
- [x] Commit all changes to git

## Key Learnings
1. MCP tool definitions require strict type validation (using Pydantic in Python)
2. Resilience patterns (timeouts, retries) are essential for external API integrations
3. Rate limit awareness prevents API throttling
4. HTTP transport with FastAPI provides a robust remote MCP server solution
5. Environment variables are the best practice for managing API keys and configuration
