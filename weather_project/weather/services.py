import requests

GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


class WeatherError(Exception):
    pass


def fetch_json(url, params):
    response = requests.get(url, params=params, timeout=5)
    response.raise_for_status()
    return response.json()


def get_weather(city):
    try:
        geo = fetch_json(GEO_URL, {"name": city, "count": 1, "language": "es"})
        results = geo.get("results")
        if not results:
            raise WeatherError(f"No se encontró la ciudad '{city}'")

        place = results[0]
        forecast = fetch_json(FORECAST_URL, {
            "latitude": place["latitude"],
            "longitude": place["longitude"],
            "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
            "timezone": "auto",
        })
    except requests.RequestException:
        raise WeatherError("El servicio del clima no está disponible")

    daily = forecast["daily"]
    return {
        "city": place["name"],
        "country": place.get("country", ""),
        "current": forecast["current"],
        "days": [
            {"date": d, "tmin": mn, "tmax": mx, "rain": r}
            for d, mn, mx, r in zip(
                daily["time"],
                daily["temperature_2m_min"],
                daily["temperature_2m_max"],
                daily["precipitation_sum"],
            )
        ],
    }