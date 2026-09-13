import os
from html import escape
from pathlib import Path

import requests
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles


API_KEY = os.getenv("WEATHER_API_KEY")
OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
BASE_DIR = Path(__file__).resolve().parent
TEMPLATE_PATH = BASE_DIR / "templates" / "index.html"

app = FastAPI(title="Skyline Weather")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


@app.get("/", response_class=FileResponse)
def home() -> FileResponse:
	return FileResponse(TEMPLATE_PATH)


@app.get("/api/weather")
def weather(city: str = Query(min_length=2, max_length=80)) -> dict:
	if not API_KEY:
		raise HTTPException(status_code=503, detail="Set WEATHER_API_KEY before searching for weather.")

	try:
		response = requests.get(
			OPENWEATHER_URL,
			params={"q": city, "appid": API_KEY, "units": "metric"},
			timeout=10,
		)
		response.raise_for_status()
		data = response.json()
	except requests.HTTPError as error:
		if error.response is not None and error.response.status_code == 404:
			raise HTTPException(status_code=404, detail=f'No weather found for "{escape(city)}".') from error
		raise HTTPException(status_code=502, detail="OpenWeather could not provide weather right now.") from error
	except requests.RequestException as error:
		raise HTTPException(status_code=502, detail="OpenWeather is temporarily unavailable.") from error

	return {
		"city": data["name"],
		"country": data["sys"]["country"],
		"temperature": data["main"]["temp"],
		"feels_like": data["main"]["feels_like"],
		"humidity": data["main"]["humidity"],
		"pressure": data["main"]["pressure"],
		"wind_speed": data["wind"]["speed"],
		"visibility": round(data.get("visibility", 0) / 1000, 1),
		"clouds": data["clouds"]["all"],
		"description": data["weather"][0]["description"],
		"icon": data["weather"][0]["icon"],
	}
