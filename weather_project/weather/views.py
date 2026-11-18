from django.shortcuts import render
from .services import get_weather, WeatherError


def index(request):
    context = {}
    city = request.GET.get("city", "").strip()

    if city:
        try:
            context.update(get_weather(city))
        except WeatherError as e:
            context["error"] = str(e)

    return render(request, "weather/index.html", context)