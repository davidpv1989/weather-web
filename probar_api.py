import json
import requests

GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


def mostrar(titulo, datos):
    print(f"\n===== {titulo} =====")
    print(json.dumps(datos, indent=2, ensure_ascii=False))


city = input("Ciudad: ").strip()

# 1) Geocodificación: nombre de ciudad -> coordenadas
geo_response = requests.get(
    GEO_URL,
    params={"name": city, "count": 1, "language": "es"},
    timeout=5,
)
print("URL llamada:", geo_response.url)
print("Código HTTP:", geo_response.status_code)
geo = geo_response.json()
mostrar("RESPUESTA DE GEOCODIFICACIÓN", geo)

if "results" not in geo:
    print("\nNo se encontró la ciudad.")
    raise SystemExit

place = geo["results"][0]

# 2) Pronóstico: coordenadas -> clima
forecast_response = requests.get(
    FORECAST_URL,
    params={
        "latitude": place["latitude"],
        "longitude": place["longitude"],
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": "auto",
    },
    timeout=5,
)
print("\nURL llamada:", forecast_response.url)
print("Código HTTP:", forecast_response.status_code)
mostrar("RESPUESTA DEL PRONÓSTICO", forecast_response.json())