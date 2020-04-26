"""standard library"""
import os
import json
import requests
from datetime import datetime

"""third party modules"""
import click

"""internal statsapi modules"""
from src.main import pass_environment, VERSION, STATSAPI_URL
from src.lib import (
    write_json_to_file,
    get_re24,
)

FILENAME = "lookup_re24_" + datetime.today().strftime('%Y_%m_%d_%H_%M_%S') + ".json"

@click.command("lookup-re24", short_help="Lookup RE24 values by year.")
@click.option(
    "--year",
    required=True,
    help="Year for looking up RE24 values."
)
@click.option(
    "--output",
    help="Location for the output file.",
    default=".",
    type=click.Path(exists=True)
)
@pass_environment
def cli(ctx, year, output):
    """lookup-re24 searches for RE24 values based on specified year. Only values starting in 2001 are available.

    Ex. statsapi lookup-re24 --year 2001 --output ./output_dir"""

    output_path = output + "/" + FILENAME

    ctx.log("+ Retrieving RE24 values for year = {0}...".format(year))

    re24 = get_re24(year)
    if not re24:
        ctx.log(
            "Command only works for 2001 to the last season, not year = {0}.".format(
                year
            ),
            level="error",
        )
        raise click.UsageError("Failed to make request.")

    try:
        re24_with_headers = []
        keys = ['NUM', 'LVL', 'YEAR', 'RUNNERS', 'EXP_R_OUTS_0', 'EXP_R_OUTS_1', 'EXP_R_OUTS_2']
        for row in re24:
            row[0] = int(row[0])
            row[2] = int(row[2])
            row[3] = int(row[3])
            row[4] = float(row[4])
            row[5] = float(row[5])
            row[6] = float(row[6])
            zipObj = zip(keys, row)
            re24_with_headers.append(dict(zipObj))
    except:
        ctx.log(
            "Could not retrieve RE24 values for year = {0}.".format(
                year
            ),
            level="error",
        )
        raise click.UsageError("Failed to make request.")


    ctx.log("+ Writing RE24 values to {0}...".format(output_path))

    write_json_to_file(re24_with_headers, output_path)

    ctx.log("Complete")
