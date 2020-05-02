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

FILENAME = "get_re24_" + datetime.today().strftime("%Y_%m_%d_%H_%M_%S") + ".json"


@click.command(
    "get-re24",
    short_help="Get play by play of a specific game with RE24 for each play.",
)
@click.option("--game-pk", required=True, help="Game PK for calculating RE24.")
@click.option(
    "--output",
    help="Location for the output file.",
    default=".",
    type=click.Path(exists=True),
)
@pass_environment
def cli(ctx, game_pk, output):
    """get-re24 play by play for a single game with calculated RE24. Play by play data only exists starting in 2001, due to data limitations this command only works starting in 2003.

    Ex. statsapi get-re24 --game-pk 566180 --output ./output_dir"""

    output_path = output + "/" + FILENAME

    ctx.log("+ Retrieving play by play for game PK {0}...".format(game_pk))

    try:
        url = STATSAPI_URL + "/game/" + game_pk + "/playByPlay"
        r = requests.get(url=url)
        data = r.json()
    except:
        ctx.log(
            "Could not get play by play for game PK = {0}.".format(game_pk),
            level="error",
        )
        raise click.UsageError("Failed to make request.")

    ctx.log("+ Calculating RE24 for game PK {0}...".format(game_pk))

    # Newer play by plays have the datetime in the play by play
    try:
        year = datetime.strptime(
            data["allPlays"][0]["about"]["endTime"], "%Y-%m-%dT%H:%M:%S.%fZ"
        ).year
    # Older play by plays do not have a datetime, so retrieve it from the game's feed
    except:
        try:
            game_url = STATSAPI_URL + "/game/" + game_pk + "/feed/live"
            game_r = requests.get(url=game_url)
            game_data = game_r.json()
            year = datetime.strptime(
                game_data["gameData"]["datetime"]["dateTime"], "%Y-%m-%dT%H:%M:%SZ"
            ).year
        except:
            ctx.log(
                "Could not get year for game PK = {0}.".format(game_pk), level="error",
            )
            raise click.UsageError("Failed to make request.")

    re24 = get_re24(year)
    if not re24:
        ctx.log(
            "Command only works for 2001 and after, not year = {0}.".format(year),
            level="error",
        )
        raise click.UsageError("Failed to make request.")

    prev_half = "top"
    prev_outs = 0
    prev_home_score = 0
    prev_away_score = 0
    prev_first = None
    prev_second = None
    prev_third = None

    # TODO: Things I might not be capturing properly
    # stolen bases, caught stealing, wild pitches, passed balls in the middle of an at bat
    try:
        for play in data["allPlays"]:
            # Pull relevant play data
            half = play["about"]["halfInning"]
            away_score = play["result"]["awayScore"]
            home_score = play["result"]["homeScore"]
            outs = play["count"]["outs"]

            # TODO: postOnFirst, Second, Third only exists starting in 2003
            # create way of calculating based on runners[] for 2001 and 2002
            first = play["matchup"].get("postOnFirst")
            second = play["matchup"].get("postOnSecond")
            third = play["matchup"].get("postOnThird")

            # If its a new half inning reset prev_outs
            if prev_half != half:
                prev_outs = 0

            # Calculate runs scored on play
            if play["about"]["isScoringPlay"] == False:
                runs_scored = 0
            elif half == "top":
                runs_scored = away_score - prev_away_score
            elif half == "bottom":
                runs_scored = home_score - prev_home_score

            # Look up start RE24 based on situation
            prev_runners = 0
            if prev_first != None:
                prev_runners += 100
            if prev_second != None:
                prev_runners += 20
            if prev_third != None:
                prev_runners += 3

            start_re24 = [re24 for re24 in re24 if re24[3] == str(prev_runners)][0]
            if prev_outs == 0:
                start_re24 = start_re24[4]
            elif prev_outs == 1:
                start_re24 = start_re24[5]
            elif prev_outs == 2:
                start_re24 = start_re24[6]

            # Look up end RE24 based on situation
            runners = 0
            if first != None:
                runners += 100
            if second != None:
                runners += 20
            if third != None:
                runners += 3

            if outs == 3:
                end_re24 = "0"
            else:
                end_re24 = [re24 for re24 in re24 if re24[3] == str(runners)][0]
                if outs == 0:
                    end_re24 = end_re24[4]
                elif outs == 1:
                    end_re24 = end_re24[5]
                elif outs == 2:
                    end_re24 = end_re24[6]

            # Calculate RE24
            final_re24 = float(end_re24) - float(start_re24) + runs_scored

            # Update the data with RE24
            play.update({"re24": final_re24})

            # Keep track of the previous play's data
            prev_half = half
            prev_outs = outs
            prev_home_score = home_score
            prev_away_score = away_score
            prev_first = first
            prev_second = second
            prev_third = third
    except:
        ctx.log(
            "Could not calculate RE24 for game PK = {0}.".format(game_pk),
            level="error",
        )
        raise click.UsageError("Failed to make request.")

    ctx.log("+ Writing RE24 play by play to {0}...".format(output_path))

    write_json_to_file(data["allPlays"], output_path)

    ctx.log("Complete")
