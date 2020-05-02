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

FILENAME = "lookup_players_" + datetime.today().strftime("%Y_%m_%d_%H_%M_%S") + ".json"


@click.command("lookup-players", short_help="Lookup players by a value.")
@click.option(
    "--value", required=True, help="The value to search for in player profiles."
)
@click.option("--game-type", help="Game type.", default="R", show_default=True)
@click.option(
    "--season",
    help="The season's year.",
    default=datetime.now().year,
    show_default=True,
)
@click.option("--sport-id", help="Sport ID, MLB = 1", default=1, show_default=True)
@click.option(
    "--output",
    help="Location for the output file.",
    default=".",
    type=click.Path(exists=True),
)
@pass_environment
def cli(ctx, value, game_type, season, sport_id, output):
    """lookup-players searches for players with the specified value in their profiles.

    Ex. statsapi lookup-players --value "Bryce Harper" --game-type R --season 2019 --sport-id 1 --output ./output_dir"""

    output_path = output + "/" + FILENAME

    ctx.log("+ Retrieving and filtering players...")

    try:
        url = STATSAPI_URL + "/sports/" + str(sport_id) + "/players"
        params = {"season": season, "gameType": game_type}
        r = requests.get(url=url, params=params)
        data = r.json()
    except:
        ctx.log(
            "Could not lookup players with value = {0}, game-type = {1}, season = {2}, and sport-id = {3}.".format(
                value, game_type, season, sport_id
            ),
            level="error",
        )
        raise click.UsageError("Failed to make request.")

    players = []
    for player in data["people"]:
        for v in player.values():
            if str(value).lower() in str(v).lower():
                players.append(player)
                break

    ctx.log("+ Writing players' information to {0}...".format(output_path))

    write_json_to_file(players, output_path)

    ctx.log("Complete")
