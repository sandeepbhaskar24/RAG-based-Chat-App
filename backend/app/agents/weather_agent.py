"""Agent 3 - live weather via Open-Meteo (free, no API key).

weather_agent --tool call--> weather_tools --> weather_agent (writes the streamed reply)
"""
from typing import Literal

import httpx
from langchain_core.messages import SystemMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool
from langgraph.graph import END
from langgraph.prebuilt import ToolNode

from app.agents.llm import get_llm
from app.agents.prompts import WEATHER_PROMPT
from app.agents.state import AgentState
from app.core.config import settings

GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

WMO = {
    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast", 45: "Fog", 48: "Rime fog",
    51: "Light drizzle", 53: "Drizzle", 55: "Dense drizzle", 56: "Freezing drizzle", 57: "Heavy freezing drizzle",
    61: "Light rain", 63: "Rain", 65: "Heavy rain", 66: "Freezing rain", 67: "Heavy freezing rain",
    71: "Light snow", 73: "Snow", 75: "Heavy snow", 77: "Snow grains",
    80: "Light rain showers", 81: "Rain showers", 82: "Violent rain showers",
    85: "Light snow showers", 86: "Heavy snow showers",
    95: "Thunderstorm", 96: "Thunderstorm with hail", 99: "Thunderstorm with heavy hail",
}


def _geocode(location: str) -> dict | None:
    """'Springfield, Illinois' -> search 'Springfield', prefer the result matching 'Illinois'."""
    name, _, hint = (p.strip() for p in location.partition(","))
    r = httpx.get(GEO_URL, params={"name": name, "count": 10, "language": "en", "format": "json"},
                  timeout=settings.WEATHER_TIMEOUT)
    r.raise_for_status()
    results = r.json().get("results") or []
    if hint:
        h = hint.lower()
        for res in results:
            hay = " ".join(str(res.get(k, "")) for k in ("admin1", "admin2", "country", "country_code")).lower()
            if h in hay:
                return res
    return results[0] if results else None


@tool
def get_weather(location: str, units: Literal["metric", "imperial"] = "metric",
                forecast_days: int = 3) -> str:
    """Get LIVE weather for a city or place: current conditions plus a short daily forecast.
    `location` can be 'Indore' or 'Springfield, Illinois' (add region/country to disambiguate).
    Use units='imperial' only if the user wants Fahrenheit/mph."""
    try:
        place = _geocode(location)
        if place is None:
            return f"Could not find a place called '{location}'. Ask the user for a more specific location."
        params = {
            "latitude": place["latitude"], "longitude": place["longitude"], "timezone": "auto",
            "forecast_days": max(1, min(forecast_days, 7)),
            "current": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,"
                       "weather_code,cloud_cover,wind_speed_10m,wind_direction_10m",
            "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max",
        }
        if units == "imperial":
            params.update(temperature_unit="fahrenheit", wind_speed_unit="mph", precipitation_unit="inch")
        r = httpx.get(FORECAST_URL, params=params, timeout=settings.WEATHER_TIMEOUT)
        r.raise_for_status()
        data = r.json()
    except httpx.HTTPError as exc:
        return f"Weather service error: {exc}. Tell the user live weather is unavailable right now."

    cur, u, daily = data["current"], data["current_units"], data["daily"]
    region = ", ".join(str(p) for p in (place.get("name"), place.get("admin1"), place.get("country")) if p)
    lines = [
        f"Location: {region} ({place['latitude']:.2f}, {place['longitude']:.2f})",
        f"Observed: {cur['time']} local time ({data.get('timezone', '')})",
        f"Conditions: {WMO.get(cur['weather_code'], 'Unknown')}",
        f"Temperature: {cur['temperature_2m']}{u['temperature_2m']} "
        f"(feels like {cur['apparent_temperature']}{u['apparent_temperature']})",
        f"Humidity: {cur['relative_humidity_2m']}% | Cloud cover: {cur['cloud_cover']}%",
        f"Wind: {cur['wind_speed_10m']} {u['wind_speed_10m']} from {cur['wind_direction_10m']}°",
        f"Precipitation (last hour): {cur['precipitation']} {u['precipitation']}",
        "Forecast:",
    ]
    for i, day in enumerate(daily["time"]):
        lines.append(
            f"- {day}: {WMO.get(daily['weather_code'][i], 'Unknown')}, "
            f"{daily['temperature_2m_min'][i]}-{daily['temperature_2m_max'][i]}{u['temperature_2m']}, "
            f"rain chance {daily['precipitation_probability_max'][i]}%")
    return "\n".join(lines)


WEATHER_TOOLS = [get_weather]
weather_tool_node = ToolNode(WEATHER_TOOLS)


def weather_agent_node(state: AgentState, config: RunnableConfig):
    llm = get_llm(0.3).bind_tools(WEATHER_TOOLS)
    reply = llm.invoke(
        [SystemMessage(WEATHER_PROMPT), *state["history"][-6:], *state["messages"]], config)
    return {"messages": [reply], "steps": state.get("steps", 0) + 1}


def route_after_weather_agent(state: AgentState) -> str:
    if getattr(state["messages"][-1], "tool_calls", None) and state.get("steps", 0) < 4:
        return "weather_tools"
    return END