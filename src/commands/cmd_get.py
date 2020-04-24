"""standard library"""
import os
import json
import requests
from datetime import datetime

"""third party modules"""
import click

"""internal statsapi modules"""
from src.main import pass_environment, VERSION, STATSAPI_URL

@click.command("get", short_help="Get response directly from statsapi.")
@click.option(
    "--module",
    required=True,
    help="The module from statsapi."
)
@click.option(
    "--params",
    help="The API parameters to pass to statsapi.",
    default=None
)
@click.option(
    "--output",
    help="Location for the output file.",
    default=".",
    type=click.Path(exists=True)
)
@pass_environment
def cli(ctx, module, params, output):
    """get sends a request directly to the statsapi module with the parameters specified.

    Ex. statsapi get --module schedule --params '{"sportId": 1, "startDate": "4/1/2019", "endDate": "4/30/2019"}' --output ./output_dir"""

    filename = "get_" + module + "_" + datetime.today().strftime('%Y_%m_%d_%H_%M_%S') + ".json"
    output_path = output + "/" + filename

    ctx.log("+ Retrieving get request for {0} module...".format(module))

    url = STATSAPI_URL + "/" + module
    parameters = json.loads(params.replace("\'","\""))
    r = requests.get(url = url, params = parameters)
    data = r.json()

    ctx.log("+ Writing get response to {0}...".format(output_path))

    file = open(output_path, "w")
    n = file.write(json.dumps(data, sort_keys=True, indent=4))
    file.close()

    ctx.log("Complete")
