# Skyline Weather

A small FastAPI web application that displays current weather from OpenWeather.

## Run locally

1. Install dependencies:

	```powershell
	pip install fastapi uvicorn requests
	```

2. Create an OpenWeather API key and set it in PowerShell:

	```powershell
	$env:WEATHER_API_KEY = "your-api-key"
	```

3. Start the app:

	```powershell
	uvicorn app:app --reload
	```

Open `http://127.0.0.1:8000` in your browser.
