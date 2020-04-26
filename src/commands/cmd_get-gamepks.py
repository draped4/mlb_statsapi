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

FILENAME = "get_gamepks_" + datetime.today().strftime("%Y_%m_%d_%H_%M_%S") + ".json"


@click.command("get-gamepks", short_help="Get game pks for a date range from statsapi.")
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
    """get-gamepks retrieves game pks for every day within the date range.

    Ex. statsapi get-gamepks --start 04/01/2019 --end 04/30/2019 --output ./output_dir"""

    output_path = output + "/" + FILENAME

    ctx.log("+ Retrieving game pks from {0} to {1}...".format(start, end))

    try:
        url = STATSAPI_URL + "/schedule"
        params = {
            "sportId": sport_id,
            "startDate": start,
            "endDate": end,
            "fields": ["dates", "games", "gamePk", "date"],
        }
        r = requests.get(url=url, params=params)
        data = r.json()
    except:
        ctx.log(
            "Could not get game PKs with start = {0}, end = {1}, and sport-id = {2}.".format(
                start, end, sport_id
            ),
            level="error",
        )
        raise click.UsageError("Failed to make request.")

    ctx.log("+ Writing game pks to {0}...".format(output_path))

    game_pk_list = []
    for day in data["dates"]:
        for game in day["games"]:
            game_pk_list.append(game["gamePk"])

    write_json_to_file(game_pk_list, output_path)

    ctx.log("Complete")
