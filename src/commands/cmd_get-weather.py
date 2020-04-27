"""standard library"""
import os
import json
import requests
from datetime import datetime, date

"""third party modules"""
import click

"""internal statsapi modules"""
from src.main import (
    pass_environment,
    VERSION,
    STATSAPI_URL,
    WEATHERBIT_URL,
    WEATHERBIT_KEY,
)
from src.lib import write_json_to_file, get_venue_latlong

FILENAME = "get_weather_" + datetime.today().strftime("%Y_%m_%d_%H_%M_%S") + ".json"


@click.command(
    "get-weather",
    short_help="Get schedule with weather data for future games from statsapi.",
)
@click.option(
    "--start",
    help="Start date to search after, inclusive.",
    default=datetime.today().strftime("%m/%d/%Y"),
)
@click.option(
    "--end",
    help="End date to search before, inclusive.",
    default=datetime.today().strftime("%m/%d/%Y"),
)
@click.option("--sport-id", help="Sport ID, MLB = 1", default=1)
@click.option(
    "--output",
    help="Location for the output file.",
    default=".",
    type=click.Path(exists=True),
)
@pass_environment
def cli(ctx, start, end, sport_id, output):
    """get-weather retrieves schedule with weather data for games within the next 16 days from statsapi.

    Ex. statsapi get-weather --start 04/01/2020 --end 04/15/2020 --output ./output_dir"""

    # Check if a Weatherbit API key exists
    if WEATHERBIT_KEY is None:
        ctx.log(
            "No Weatherbit API key detected. Please add one to the config.json.",
            level="error",
        )
        raise click.UsageError("Failed to make request.")

    output_path = output + "/" + FILENAME

    try:
        start_date = datetime.strptime(start, "%m/%d/%Y").date()
        end_date = datetime.strptime(end, "%m/%d/%Y").date()
    except:
        ctx.log(
            "Could not parse start = {0} and/or end = {1}.".format(start, end),
            level="error",
        )
        raise click.UsageError("Failed to make request.")

    # Check if start date is not before today
    if start_date < date.today():
        ctx.log(
            "Start date cannot be before today.", level="error",
        )
        raise click.UsageError("Failed to make request.")

    # Check if end date is after start date
    if end_date < start_date:
        ctx.log(
            "End date cannot be before start date.", level="error",
        )
        raise click.UsageError("Failed to make request.")

    # Check if end date is within 16 days of today
    if (end_date - date.today()).days >= 16:
        ctx.log(
            "End date cannot be more than 16 days from today.", level="error",
        )
        raise click.UsageError("Failed to make request.")

    # Calculate number of days between the start and end dates, including both dates
    days = (end_date - start_date).days + 1

    ctx.log("+ Retrieving schedule from {0} to {1}...".format(start, end))

    try:
        url = STATSAPI_URL + "/schedule"
        params = {
            "sportId": sport_id,
            "startDate": start,
            "endDate": end,
        }
        r = requests.get(url=url, params=params)
        data = r.json()
    except:
        ctx.log(
            "Could not get schedule with start = {0}, end = {1}, and sport-id = {2}.".format(
                start, end, sport_id
            ),
            level="error",
        )
        raise click.UsageError("Failed to make request.")

    ctx.log("+ Retrieving weather from {0} to {1}...".format(start, end))

    try:
        with click.progressbar(data["dates"]) as data_dates:
            for d in data_dates:
                for game in d["games"]:
                    game_venue = game["venue"]["name"]
                    venue_latlong = get_venue_latlong(game_venue)

                    # If no latlong then continue
                    if venue_latlong is None:
                        game.update({"weather_data": "No weather found."})
                        continue

                    # Calculate number of days between the game and today to pick the right forecast
                    game_datetime = datetime.strptime(
                        game["gameDate"], "%Y-%m-%dT%H:%M:%SZ"
                    )
                    game_date = date(
                        game_datetime.year, game_datetime.month, game_datetime.day
                    )
                    days = (game_date - date.today()).days

                    # https://www.weatherbit.io/api/weather-forecast-16-day
                    weather_url = WEATHERBIT_URL + "/forecast/daily"
                    weather_params = {
                        "key": WEATHERBIT_KEY,
                        "lang": "en",
                        "units": "I",
                        "days": days + 1,
                        "lat": venue_latlong["lat"],
                        "lon": venue_latlong["long"],
                    }
                    weather_r = requests.get(url=weather_url, params=weather_params)
                    weather_data = weather_r.json()

                    # TODO: Add other weather data too
                    game.update({"weather_data": weather_data["data"][days]})
    except:
        ctx.log(
            "Could not retrieve forecast starting on {0} and ending on {1}.".format(
                start, end
            ),
            level="error",
        )
        raise click.UsageError("Failed to make request.")

    ctx.log("+ Writing schedule with weather to {0}...".format(output_path))

    write_json_to_file(data, output_path)

    ctx.log("Complete")
