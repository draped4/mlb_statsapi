"""standard library"""
import os
import json
import csv
import requests
from datetime import datetime

"""third party modules"""
import click

"""internal statsapi modules"""
from src.main import pass_environment, VERSION, STATSAPI_URL, LAHMAN_URL
from src.lib import write_json_to_file

LAHMAN_TABLES = [
    "AllstarFull",
    "Appearances",
    "AwardsManagers",
    "AwardsPlayers",
    "AwardsShareManagers",
    "AwardsSharePlayers",
    "Batting",
    "BattingPost",
    "CollegePlaying",
    "Fielding",
    "FieldingOF",
    "FieldingOFsplit",
    "FieldingPost",
    "HallOfFame",
    "HomeGames",
    "Managers",
    "ManagersHalf",
    "Parks",
    "People",
    "Pitching",
    "PitchingPost",
    "Salaries",
    "Schools",
    "SeriesPost",
    "Teams",
    "TeamsFranchises",
    "TeamsHalf",
]


@click.command("get-lahman", short_help="Get data from Lahman's baseball database.")
@click.option(
    "--table", required=True, help="Table to retrieve from Lahman's baseball database."
)
@click.option(
    "--output",
    help="Location for the output file.",
    default=".",
    type=click.Path(exists=True),
)
@pass_environment
def cli(ctx, table, output):
    """get-lahman retrieves data from Lahman's baseball database. Source: http://www.seanlahman.com/baseball-archive/statistics/.

    Ex. statsapi get-lahman --table Batting --output ./output_dir"""

    FILENAME = (
        "get_lahman_"
        + table
        + "_"
        + datetime.today().strftime("%Y_%m_%d_%H_%M_%S")
        + ".json"
    )
    output_path = output + "/" + FILENAME

    if table not in LAHMAN_TABLES:
        ctx.log(
            "No table exists with name = {0}. Select from one of {1}".format(
                table, LAHMAN_TABLES
            ),
            level="error",
        )
        raise click.UsageError("Failed to make request.")

    ctx.log("+ Retrieving Lahman data from table = {0}...".format(table))

    try:
        url = LAHMAN_URL + "/" + table + ".csv"
        r = requests.get(url=url)

        reader = csv.reader(r.text.split("\n"), delimiter=",")
        data_json = []
        keys = []
        count = 0
        for row in reader:
            if count == 0:
                keys = row
                count += 1
            else:
                zipObj = zip(keys, row)
                data_json.append(dict(zipObj))
    except:
        ctx.log(
            "Could not find data for table = {0}.".format(table), level="error",
        )
        raise click.UsageError("Failed to make request.")

    ctx.log("+ Writing Lahman data to {0}...".format(output_path))

    write_json_to_file(data_json, output_path)

    ctx.log("Complete")
