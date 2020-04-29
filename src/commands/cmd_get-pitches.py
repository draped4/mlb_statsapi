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

FILENAME = "get_pitches_" + datetime.today().strftime("%Y_%m_%d_%H_%M_%S") + ".json"
FILENAME_CSV = "get_pitches_" + datetime.today().strftime("%Y_%m_%d_%H_%M_%S") + ".csv"


@click.command("get-pitches", short_help="Get pitches for a game from statsapi.")
@click.option("--game-pk", required=True, help="Game PK for retrieving pitches.")
@click.option(
    "--output",
    help="Location for the output file.",
    default=".",
    type=click.Path(exists=True),
)
@pass_environment
def cli(ctx, game_pk, output):
    """get-pitches retrieves pitches for a specified game PK.

    Ex. statsapi get-pitches --game-pk 566180 --output ./output_dir"""

    output_path = output + "/" + FILENAME

    ctx.log("+ Retrieving pitches for game PK = {0}...".format(game_pk))

    try:
        url = STATSAPI_URL + "/game/" + game_pk + "/playByPlay"
        r = requests.get(url=url)
        data = r.json()
    except:
        ctx.log(
            "Could not get pitches from game PK = {0}.".format(game_pk), level="error",
        )
        raise click.UsageError("Failed to make request.")

    ctx.log("+ Writing pitches to {0}...".format(output_path))

    try:
        atbat_list = []
        for play in data["allPlays"]:
            pitch_list = []
            pitch_sequence = []
            pitch_counts = []
            prev_count = {"balls": 0, "strikes": 0}

            for playEvent in play["playEvents"]:
                if playEvent["isPitch"] == True:
                    playEvent.update({"prevCount": prev_count})

                    # If there is no type.code it is becasue it is an automatic ball on an IBB
                    pitch_sequence.append(
                        playEvent["details"].get("type", {"code": "AB"})["code"]
                    )

                    pitch_list.append(playEvent)

                    prev_count = playEvent["count"]

            atbat = {
                "atBatIndex": play["atBatIndex"],
                "matchup": play["matchup"],
                "result": play["result"],
                "pitches": pitch_list,
                "pitchSequence": pitch_sequence,
            }
            atbat_list.append(atbat)
    except:
        ctx.log(
            "Could not parse pitches from game PK = {0}.".format(game_pk),
            level="error",
        )
        raise click.UsageError("Failed to make request.")

    write_json_to_file(atbat_list, output_path)

    ctx.log("Complete")
