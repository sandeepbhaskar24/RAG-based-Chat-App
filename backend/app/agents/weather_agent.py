"""Agent 3 - live weather via Open-Meteo (free, no API key).

Graph:  weather_extract -> weather_fetch -> weather_answer
        (each step can end early: no location -> ask for a city; service down -> say so)
"""
import logging
from typing import Literal

import httpx
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import END
from pydantic import BaseModel, Field

from app.agents.context import emit, get_ctx
from app.agents.llm import call_structured, stream_answer
from app.agents.prompts import WEATHER_ANSWER_PROMPT, WEATHER_EXTRACT_PROMPT
from app.agents.state import AgentState
from app.core.config import settings

logger = logging.getLogger(__name__)

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


class WeatherRequest(BaseModel):
    location: str | None = Field(default=None, description="City/place, or null if unknown")
    units: Literal["metric", "imperial"] = "metric"
    forecast_days: int = 3


class WeatherError(Exception):
    """Raised with a user-friendly message."""


def _geocode(location: str) -> dict | None:
    """'Springfield, Illinois' -> search 'Springfield', prefer the result matching 'Illinois'."""
    name, _, hint = (p.strip() for p in location.partition(","))
    r = httpx.get(GEO_URL, params={"name": name, "count": 10, "language": "en", "format": "json"},
                  timeout=settings.WEATHER_TIMEOUT)
    r.raise_for_status()
    results = r.json().get("results") or []
    if hint:
        for res in results:
            hay = " ".join(str(res.get(k, "")) for k in ("admin1", "admin2", "country", "country_code")).lower()
            if hint.lower() in hay:
                return res
    return results[0] if results else None


def fetch_weather(location: str, units: str = "metric", forecast_days: int = 3) -> str:
    """Return a plain-text weather report, or raise WeatherError."""
    try:
        place = _geocode(location)
        if place is None:
            raise WeatherError(f"I couldn't find a place called '{location}'. Could you be more specific?")
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
        logger.warning("Weather service error: %s", exc)
        raise WeatherError("Live weather is unavailable right now. Please try again in a moment.") from exc

    cur, u, daily = data["current"], data["current_units"], data["daily"]
    region = ", ".join(str(p) for p in (place.get("name"), place.get("admin1"), place.get("country")) if p)
    lines = [
        f"Location: {region}",
        f"Observed: {cur['time']} local time ({data.get('timezone', '')})",
        f"Conditions: {WMO.get(cur['weather_code'], 'Unknown')}",
        f"Temperature: {cur['temperature_2m']}{u['temperature_2m']} "
        f"(feels like {cur['apparent_temperature']}{u['apparent_temperature']})",
        f"Humidity: {cur['relative_humidity_2m']}% | Cloud cover: {cur['cloud_cover']}%",
        f"Wind: {cur['wind_speed_10m']} {u['wind_speed_10m']} from {cur['wind_direction_10m']} degrees",
        f"Precipitation (last hour): {cur['precipitation']} {u['precipitation']}",
        "Forecast:",
    ]
    for i, day in enumerate(daily["time"]):
        lines.append(
            f"- {day}: {WMO.get(daily['weather_code'][i], 'Unknown')}, "
            f"{daily['temperature_2m_min'][i]}-{daily['temperature_2m_max'][i]}{u['temperature_2m']}, "
            f"rain chance {daily['precipitation_probability_max'][i]}%")
    return "\n".join(lines)


# ── Graph nodes ─────────────────────────────────────────────────────────────────

def weather_extract_node(state: AgentState, config: RunnableConfig):
    """LLM call 1: pull the location/units out of the question (and chat history)."""
    ctx = get_ctx(config)
    try:
        req = call_structured(
            ctx.budget, "weather_extract", WeatherRequest,
            [SystemMessage(WEATHER_EXTRACT_PROMPT), *state["history"][-6:], HumanMessage(state["question"])])
    except Exception:
        logger.exception("Weather request extraction failed")
        req = WeatherRequest()

    if not req.location:
        text = "Which city would you like the weather for?"
        emit("token", text)
        return {"weather": None, "answer": text}
    return {"weather": req}


def route_after_extract(state: AgentState) -> str:
    return "fetch" if state.get("weather") else END


def weather_fetch_node(state: AgentState, config: RunnableConfig):
    """Plain HTTP call, no LLM."""
    ctx, req = get_ctx(config), state["weather"]
    emit("status", f"Fetching live weather for {req.location}\u2026")
    try:
        with ctx.stage("weather_fetch"):
            return {"report": fetch_weather(req.location, req.units, req.forecast_days)}
    except WeatherError as exc:
        emit("token", str(exc))
        return {"report": "", "answer": str(exc)}


def route_after_fetch(state: AgentState) -> str:
    return "answer" if state.get("report") else END


def weather_answer_node(state: AgentState, config: RunnableConfig):
    """LLM call 2: turn the raw report into a friendly streamed summary."""
    ctx = get_ctx(config)
    messages = [SystemMessage(WEATHER_ANSWER_PROMPT.format(report=state["report"])),
                HumanMessage(state["question"])]
    parts = []
    for text in stream_answer(ctx.budget, "weather_answer", messages, temperature=0.3):
        parts.append(text)
        emit("token", text)
    return {"answer": "".join(parts)}