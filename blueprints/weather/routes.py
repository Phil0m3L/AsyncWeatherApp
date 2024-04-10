import json
from datetime import datetime, timedelta

import aiohttp

from quart import render_template, redirect, url_for, current_app, flash

from . import weather_bp

from forms import SearchForm


@weather_bp.route("/app/current", methods=["POST"])
async def _app_current():
    search_form = await SearchForm().create_form()

    if await search_form.validate_on_submit():
        city = search_form.city.data
        temperature_unit = search_form.temperature_unit.data
        distance_unit = search_form.distance_unit.data

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://api.weatherapi.com/v1/current.json?key={current_app.config['WEATHER_API_KEY']}&q={city}"
            ) as res:
                res = await res.json()

                if "error" in res.keys() and res["error"]["code"] == 1006:
                    await flash(
                        "The city you entered is invalid. Please try again.",
                        "error",
                    )
                    return redirect(url_for("meta._index"))

                elif "current" not in res.keys():
                    await flash(
                        "An API-side error occurred while processing your request. "
                        "Please try again later.",
                        "warning",
                    )
                    return redirect(url_for("meta._index"))

                else:
                    current = res["current"]
                    location = res["location"]

                    city = location["name"].lower()
                    city_name = f"{location['name']}, {location['region']}, {location['country']}"
                    image_url = f"https:{current['condition']['icon']}"

                    city_data = {
                        "city_name": city_name,
                        "latitude": location["lat"],
                        "longitude": location["lon"],
                        "timezone": location["tz_id"].replace("/", "_"),
                        "localtime": location["localtime"],
                    }

                    date = datetime.fromtimestamp(
                        current["last_updated_epoch"]
                    ).strftime("%Y-%m-%d (%A)")
                    temperature = (
                        f"{current['temp_c']}°C"
                        if temperature_unit == "celsius"
                        else f"{current['temp_f']}°F"
                    )
                    local_time = location["localtime"]
                    last_updated = current["last_updated"]
                    condition = current["condition"]["text"]
                    feels_like = (
                        f"{current['feelslike_c']}°C"
                        if temperature_unit == "celsius"
                        else f"{current['feelslike_f']}°F"
                    )
                    humidity = f"{current['humidity']}%"
                    wind_speed = (
                        f"{current['wind_kph']} km/h"
                        if distance_unit == "kilometres"
                        else f"{current['wind_mph']} mph"
                    )
                    wind_direction = current["wind_dir"]
                    precipitation = f"{current['precip_mm']} mm"
                    pressure = f"{current['pressure_mb']} mb"
                    cloud_cover = f"{current['cloud']}%"
                    visibility = (
                        f"{current['vis_km']} km"
                        if distance_unit == "kilometres"
                        else f"{current['vis_miles']} miles"
                    )
                    uv_index = current["uv"]

                    await flash("Weather data retrieved.", "success")

                    return await render_template(
                        "weather/app.html",
                        city=city,
                        date=date,
                        temperature_unit=temperature_unit,
                        distance_unit=distance_unit,
                        city_data=city_data,
                        city_data_string=json.dumps(city_data),
                        image_url=image_url,
                        temperature=temperature,
                        local_time=local_time,
                        last_updated=last_updated,
                        condition=condition,
                        feels_like=feels_like,
                        humidity=humidity,
                        wind_speed=wind_speed,
                        wind_direction=wind_direction,
                        precipitation=precipitation,
                        pressure=pressure,
                        cloud_cover=cloud_cover,
                        visibility=visibility,
                        uv_index=uv_index,
                    )


@weather_bp.route(
    "/app/forecast/<city>/<city_data_string>/<temperature_unit>/<distance_unit>",
    methods=["GET"],
)
async def _app_forecast(
    city: str, city_data_string: str, temperature_unit: str, distance_unit: str
):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"https://api.weatherapi.com/v1/forecast.json?key={current_app.config['WEATHER_API_KEY']}"
            f"&q={city}&days=14&hour=-1"
        ) as res:
            res = await res.json()

            if "error" in res.keys() and res["error"]["code"] == 1006:
                await flash(
                    "The city you entered is invalid. Please try again.",
                    "error",
                )
                return redirect(url_for("meta._index"))

            elif "forecast" not in res.keys():
                await flash(
                    "An API-side error occurred while processing your request. "
                    "Please try again later.",
                    "warning",
                )
                return redirect(url_for("meta._index"))

            else:
                forecast = res["forecast"]

                city_data = json.loads(city_data_string)

                forecast_data = []

                for day in forecast["forecastday"]:
                    date = datetime.fromtimestamp(day["date_epoch"]).strftime(
                        "%Y-%m-%d (%A)"
                    )
                    image_url = f"https:{day['day']['condition']['icon']}"
                    sunrise = day["astro"]["sunrise"]
                    sunset = day["astro"]["sunset"]
                    min_temp = (
                        f"{day['day']['mintemp_c']}°C"
                        if temperature_unit == "celsius"
                        else f"{day['day']['mintemp_f']}°F"
                    )
                    max_temp = (
                        f"{day['day']['maxtemp_c']}°C"
                        if temperature_unit == "celsius"
                        else f"{day['day']['maxtemp_f']}°F"
                    )
                    condition = day["day"]["condition"]["text"]
                    humidity = f"{day['day']['avghumidity']}%"
                    wind_speed = (
                        f"{day['day']['maxwind_kph']} km/h"
                        if distance_unit == "kilometres"
                        else f"{day['day']['maxwind_mph']} mph"
                    )
                    precipitation = f"{day['day']['totalprecip_mm']} mm"
                    snowfall = f"{day['day']['totalsnow_cm']} cm"
                    visibility = (
                        f"{day['day']['avgvis_km']} km"
                        if distance_unit == "kilometres"
                        else f"{day['day']['avgvis_miles']} miles"
                    )
                    uv_index = day["day"]["uv"]

                    forecast_data.append(
                        {
                            "date": date,
                            "image_url": image_url,
                            "sunrise": sunrise,
                            "sunset": sunset,
                            "min_temp": min_temp,
                            "max_temp": max_temp,
                            "condition": condition,
                            "humidity": humidity,
                            "wind_speed": wind_speed,
                            "precipitation": precipitation,
                            "snowfall": snowfall,
                            "visibility": visibility,
                            "uv_index": uv_index,
                        }
                    )

                await flash("Weather forecast data retrieved.", "success")

                return await render_template(
                    "weather/forecast.html",
                    city=city,
                    city_data_string=city_data_string,
                    temperature_unit=temperature_unit,
                    distance_unit=distance_unit,
                    city_data=city_data,
                    forecast_data=forecast_data,
                )


@weather_bp.route(
    "/app/historical/<city>/<city_data_string>/<temperature_unit>/<distance_unit>",
    methods=["GET"],
)
async def _app_historical(
    city: str, city_data_string: str, temperature_unit: str, distance_unit: str
):
    day = datetime.today()
    historical_data = []

    for _ in range(14):
        day -= timedelta(days=1)
        historical_date = day.strftime("%Y-%m-%d")

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://api.weatherapi.com/v1/history.json?key={current_app.config['WEATHER_API_KEY']}"
                f"&q={city}&dt={historical_date}&hour=-1"
            ) as res:
                res = await res.json()

                if "error" in res.keys() and res["error"]["code"] == 1006:
                    await flash(
                        "The city you entered is invalid. Please try again.",
                        "error",
                    )
                    return redirect(url_for("meta._index"))

                elif "forecast" not in res.keys():
                    await flash(
                        "An API-side error occurred while processing your request. "
                        "Please try again later.",
                        "warning",
                    )
                    return redirect(url_for("meta._index"))

                else:
                    forecast = res["forecast"]["forecastday"][0]

                    city_data = json.loads(city_data_string)

                    date = datetime.fromtimestamp(forecast["date_epoch"]).strftime(
                        "%Y-%m-%d (%A)"
                    )
                    image_url = f"https:{forecast['day']['condition']['icon']}"
                    sunrise = forecast["astro"]["sunrise"]
                    sunset = forecast["astro"]["sunset"]
                    min_temp = (
                        f"{forecast['day']['mintemp_c']}°C"
                        if temperature_unit == "celsius"
                        else f"{forecast['day']['mintemp_f']}°F"
                    )
                    max_temp = (
                        f"{forecast['day']['maxtemp_c']}°C"
                        if temperature_unit == "celsius"
                        else f"{forecast['day']['maxtemp_f']}°F"
                    )
                    condition = forecast["day"]["condition"]["text"]
                    humidity = f"{forecast['day']['avghumidity']}%"
                    wind_speed = (
                        f"{forecast['day']['maxwind_kph']} km/h"
                        if distance_unit == "kilometres"
                        else f"{forecast['day']['maxwind_mph']} mph"
                    )
                    precipitation = f"{forecast['day']['totalprecip_mm']} mm"
                    snowfall = f"{forecast['day']['totalsnow_cm']} cm"
                    visibility = (
                        f"{forecast['day']['avgvis_km']} km"
                        if distance_unit == "kilometres"
                        else f"{forecast['day']['avgvis_miles']} miles"
                    )
                    uv_index = forecast["day"]["uv"]

                    historical_data.append(
                        {
                            "date": date,
                            "image_url": image_url,
                            "sunrise": sunrise,
                            "sunset": sunset,
                            "min_temp": min_temp,
                            "max_temp": max_temp,
                            "condition": condition,
                            "humidity": humidity,
                            "wind_speed": wind_speed,
                            "precipitation": precipitation,
                            "snowfall": snowfall,
                            "visibility": visibility,
                            "uv_index": uv_index,
                        }
                    )

    await flash("Historical weather data retrieved.", "success")

    return await render_template(
        "weather/historical.html",
        city=city,
        city_data_string=city_data_string,
        temperature_unit=temperature_unit,
        distance_unit=distance_unit,
        city_data=city_data,
        historical_data=historical_data,
    )
