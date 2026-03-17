# Week 3 - OpenWeatherMap MCP Server: Key Learnings

## [x] 1. Project Setup

- **Chosen API:** OpenWeatherMap current weather and forecast API
  - Free tier available: 60 calls per minute, no credit card required
  - Public and well-documented
  - Useful real-world data that can be used by assistants

- **Deployment Mode:** Local STDIO (simpler for Claude Desktop integration)
  - STDIO transport is simpler than HTTP for local use
  - Meets the requirement of 2+ tools

## [x] 2. Implementation Details

**Files created:**
- `week3/server/server.py` - Main MCP server implementation
- `week3/README.md` - Complete setup instructions and tool reference for Claude Desktop
- `week3/requirements.txt` - Dependencies list
- `week3/plan.md` - This document

**Tools implemented:**
- `get_current_weather(city, country_code?)` - Gets current weather with detailed metrics
- `get_forecast(city, country_code?, days?)` - Gets multi-day forecast with 3-hour intervals

## [x] 3. Resilience Features

| Requirement | Status |
|-------------|--------|
| Graceful error handling | ✅ Handles 401 (bad key), 404 (city not found), 429 (rate limit), timeout |
| Timeout protection | ✅ 10 second timeout |
| Rate limit awareness | ✅ Passes through 429 errors cleanly |
| Correct logging | ✅ All logs go to stderr, doesn't pollute STDIO JSON |

## [x] 4. MCP Implementation Notes

- Uses the official MCP SDK (`mcp` package)
- Pydantic models for parameter validation
- JSON schema automatically generated from models for tool listing
- Async/await for I/O concurrency
- Clean closing of HTTP client after each request

## [x] 5. Key Learnings

1. **STDIO transport constraints:**
   - Must *not* write anything to stdout except MCP JSON messages
   - All logging must go to stderr
   - This is critical - any extra stdout breaks the protocol parsing

2. **Error handling:**
   - Always validate API key presence before making requests
   - Return human-readable error messages that the LLM can understand
   - Different error status codes need different messages for better debugging

3. **Parameter design:**
   - Optional `country_code` helps disambiguate cities with same name (e.g., Portland US vs Portland UK)
   - Pydantic validation catches bad inputs before they reach the API

## Summary

| Requirement | Done |
|-------------|------|
| Choose external API | ✅ OpenWeatherMap |
| Expose 2+ MCP tools | ✅ get_current_weather, get_forecast |
| Basic resilience | ✅ Errors, timeout, rate limit |
| Packaging/docs | ✅ README with setup instructions |
| Local STDIO deployment | ✅ Ready for Claude Desktop |
| Documentation | ✅ `plan.md` complete ✓ |

**Total:** All requirements satisfied. Server is ready to use.
