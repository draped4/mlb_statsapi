"""standard library"""
import os
import json
import requests
from datetime import datetime

"""third party modules"""
import click

"""internal statsapi modules"""
from src.main import pass_environment, VERSION, STATSAPI_URL

FILENAME = "get_gamepks_" + datetime.today().strftime('%Y_%m_%d_%H_%M_%S') + ".json"

@click.command("get-gamepks", short_help="Get game pks for a date range from statsapi.")
@click.option(
    "--start",
    required=True,
    help="Start date to search after, inclusive."
)
@click.option(
    "--end",
    help="End date to search before, inclusive.",
    default=datetime.today().strftime('%m/%d/%Y')
)
@click.option(
    "--sport-id",
    help="Sport ID, MLB = 1",
    default=1
)
@click.option(
    "--output",
    help="Location for the output file.",
    default=".",
    type=click.Path(exists=True)
)
@pass_environment
def cli(ctx, start, end, sport_id, output):
    """get-gamepks retrieves game pks for every day within the date range.

    Ex. statsapi get-gamepks --start 04/01/2019 --end 04/30/2019 --output ./output_dir"""

    output_path = output + "/" + FILENAME

    ctx.log("+ Retrieving game pks from {0} to {1}...".format(start, end))

    url = STATSAPI_URL + "/schedule"
    params = {'sportId': sport_id, 'startDate': start, 'endDate': end, 'fields': ['dates','games','gamePk','date']}
    r = requests.get(url = url, params = params)
    data = r.json()

    ctx.log("+ Writing game pks to {0}...".format(output_path))

    game_pk_list = []
    for day in data['dates']:
    	for game in day['games']:
    		game_pk_list.append(game['gamePk'])

    file = open(output_path, "w")
    n = file.write(json.dumps(game_pk_list, sort_keys=True, indent=4))
    file.close()

    ctx.log("Complete")
