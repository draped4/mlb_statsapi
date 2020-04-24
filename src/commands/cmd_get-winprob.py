"""standard library"""
import os
import json
import requests
from datetime import datetime

"""third party modules"""
import click

"""internal statsapi modules"""
from src.main import pass_environment, VERSION, STATSAPI_URL

FILENAME = "get_winprob_" + datetime.today().strftime('%Y_%m_%d_%H_%M_%S') + ".json"

@click.command("get-winprob", short_help="Get win probabilities per plate appearance for a game from statsapi.")
@click.option(
    "--game-pk",
    required=True,
    help="Game PK for retrieving win probabilities."
)
@click.option(
    "--output",
    help="Location for the output file.",
    default=".",
    type=click.Path(exists=True)
)
@pass_environment
def cli(ctx, game_pk, output):
    """get-winprob retrieves win probabilities for a game.

    Ex. statsapi get-winprob --game-pk 566180 --output ./output_dir"""

    output_path = output + "/" + FILENAME

    ctx.log("+ Retrieving win probabilities from {0}...".format(game_pk))

    url = STATSAPI_URL + "/game/" + game_pk + "/winProbability"
    params = {'fields': ['atBatIndex','playEndTime','homeTeamWinProbability','awayTeamWinProbability','homeTeamWinProbabilityAdded']}
    r = requests.get(url = url, params = params)
    data = r.json()

    ctx.log("+ Writing win probabilities to {0}...".format(output_path))

    file = open(output_path, "w")
    n = file.write(json.dumps(data, sort_keys=True, indent=4))
    file.close()

    ctx.log("Complete")
