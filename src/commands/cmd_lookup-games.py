"""standard library"""
import os
import json
import requests
from datetime import datetime

"""third party modules"""
import click

"""internal statsapi modules"""
from src.main import pass_environment, VERSION, STATSAPI_URL
from src.lib import write_json_to_file

FILENAME = "lookup_games_" + datetime.today().strftime("%Y_%m_%d_%H_%M_%S") + ".json"


@click.command("lookup-games", short_help="Lookup games by a value.")
@click.option(
    "--value", required=True, help="The value to search for in game profiles."
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
def cli(ctx, value, start, end, sport_id, output):
    """lookup-games searches for games with the specified value in their profiles.

    Ex. statsapi lookup-games --value "Indians" --start 4/1/2019 --end 4/30/2020 --sport-id 1 --output ./output_dir"""

    output_path = output + "/" + FILENAME

    ctx.log("+ Retrieving and filtering games...")

    try:
        url = STATSAPI_URL + "/schedule"
        params = {"sportId": sport_id, "startDate": start, "endDate": end}
        r = requests.get(url=url, params=params)
        data = r.json()
    except:
        ctx.log(
            "Could not lookup games with value = {0}, start = {1}, end = {2}, and sport-id = {3}.".format(
                value, start, end, sport_id
            ),
            level="error",
        )
        raise click.UsageError("Failed to make request.")

    games = []
    for day in data["dates"]:
        for game in day["games"]:
            for v in game.values():
                if str(value).lower() in str(v).lower():
                    games.append(game)
                    break

    ctx.log("+ Writing games' information to {0}...".format(output_path))

    write_json_to_file(games, output_path)

    ctx.log("Complete")
