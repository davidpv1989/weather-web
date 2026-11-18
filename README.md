# Weather web

Aplicación web de práctica para aprender el framework **Django** (patrón MVT: Model–View–Template). Permite buscar una ciudad y ver su clima actual y el pronóstico de varios días, consultando una API externa con Python.

No usa base de datos, por eso no tiene Models: la vista obtiene los datos de la API y los entrega a la plantilla.

## Estructura

```
Weather web
├── venv/
├── probar_api.py              # script para ver la respuesta de la API sin Django
└── weather_project
    ├── manage.py
    ├── weather_project/       # configuración del proyecto (settings.py, urls.py)
    └── weather/               # app del clima
        ├── services.py        # llamadas a la API
        ├── views.py           # lógica de la vista
        ├── urls.py            # rutas de la app
        └── templates/weather/index.html
```

## Instalación y ejecución (Windows, PowerShell)

```powershell
cd "C:\Users\orlan\Documents\Weather web"
python -m venv venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
venv\Scripts\activate
pip install django requests
cd weather_project
python manage.py runserver
```

Abrir http://127.0.0.1:8000/ y buscar una ciudad.

## Cómo funciona

1. El navegador pide `/?city=Santiago`.
2. `urls.py` dirige la petición a `views.index`.
3. La vista llama a `services.get_weather(city)`, que consulta la API en dos pasos.
4. La vista entrega los datos a `index.html`, que genera la página.

## API utilizada: Open-Meteo

[Open-Meteo](https://open-meteo.com/) es gratuita y no requiere API key. Documentación:

- Pronóstico: https://open-meteo.com/en/docs
- Geocodificación: https://open-meteo.com/en/docs/geocoding-api

Ambas son peticiones `GET` que devuelven JSON.

### 1. Geocodificación (nombre de ciudad → coordenadas)

```
GET https://geocoding-api.open-meteo.com/v1/search
```

| Parámetro  | Descripción                                |
|------------|--------------------------------------------|
| `name`     | Nombre de la ciudad (obligatorio)          |
| `count`    | Cantidad máxima de resultados (usamos 1)   |
| `language` | Idioma de los nombres (usamos `es`)        |

Respuesta: un objeto con la lista `results`. Si la ciudad no existe, `results` no aparece. Campos principales de cada resultado:

| Campo                     | Descripción                       |
|---------------------------|-----------------------------------|
| `id`                      | Identificador de la ubicación     |
| `name`                    | Nombre de la ciudad               |
| `latitude` / `longitude`  | Coordenadas                       |
| `country`                 | País                              |
| `timezone`                | Zona horaria                      |
| `elevation`               | Altitud en metros                 |
| `population`              | Población                         |

### 2. Pronóstico (coordenadas → clima)

```
GET https://api.open-meteo.com/v1/forecast
```

| Parámetro   | Valor que usamos                                                   |
|-------------|--------------------------------------------------------------------|
| `latitude`, `longitude` | Coordenadas obtenidas en el paso anterior              |
| `current`   | `temperature_2m,relative_humidity_2m,wind_speed_10m`               |
| `daily`     | `temperature_2m_max,temperature_2m_min,precipitation_sum`          |
| `timezone`  | `auto` (usa la zona horaria de las coordenadas)                    |

Estructura de la respuesta:

| Campo                       | Contenido                                                      |
|-----------------------------|----------------------------------------------------------------|
| `latitude`, `longitude`, `elevation`, `timezone` | Datos de la ubicación consultada          |
| `current_units`             | Unidad de cada variable de `current`                           |
| `current`                   | Valores actuales: `time` más cada variable pedida              |
| `daily_units`               | Unidad de cada variable de `daily`                             |
| `daily`                     | Listas paralelas: `time` (fechas) y una lista por variable     |

Variables que usamos:

| Variable               | Bloque  | Significado                          | Unidad |
|------------------------|---------|--------------------------------------|--------|
| `temperature_2m`       | current | Temperatura a 2 m del suelo          | °C     |
| `relative_humidity_2m` | current | Humedad relativa                     | %      |
| `wind_speed_10m`       | current | Velocidad del viento a 10 m          | km/h   |
| `temperature_2m_max`   | daily   | Temperatura máxima del día           | °C     |
| `temperature_2m_min`   | daily   | Temperatura mínima del día           | °C     |
| `precipitation_sum`    | daily   | Precipitación total del día          | mm     |

En `daily`, cada lista tiene un valor por día y todas están alineadas con `time`. Por eso el código las junta con `zip`.

Se pueden pedir más variables marcándolas en la documentación del pronóstico. Para ver la respuesta completa sin Django, ejecutar `probar_api.py`:

```powershell
venv\Scripts\python.exe probar_api.py
```

## Licencia de los datos

Open-Meteo es de uso no comercial y pide atribución ("Weather data by Open-Meteo.com") si se publican sus datos. Este proyecto es solo de práctica.