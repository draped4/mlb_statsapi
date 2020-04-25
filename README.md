# CLI Tool for MLB's StatsAPI

`statsapi` is a standardized tool that can be used to download data from
MLB StatsAPI directly from the CLI. It was developed using a python package, [Click](https://click.palletsprojects.com/en/7.x/).

## Development & Setup

To run the CLI tool locally on macOS or Linux execute the following CLI commands:
```sh
$ cd mlb_statsapi/
$ pip install virtualenv
$ virtualenv venv
$ . venv/bin/activate
$ pip install -r requirements.txt
$ pip install --editable .
```

The `--editable` flag will allow for you to make edits to code without having to
re-run `pip install ...` locally.

Run `statsapi --version` to verify the installation was successful.
```sh
$ statsapi --version
statsapi version: v0.1.0
```

## CLI Commands
### `statsapi --help`
```sh
$ statsapi --help
Usage: statsapi [OPTIONS] COMMAND [ARGS]...

  Statsapi is the standardized tool that can be used to download data from
  MLB statsapi.

Options:
  --home DIRECTORY  Project folder to operate on.
  -v, --verbose     Enables verbose mode.
  --version         Print the current version of statsapi.
  --help            Show this message and exit.

Commands:
  get             Get response directly from statsapi.
  get-gamepks     Get game pks for a date range from statsapi.
  get-winprob     Get win probabilities per plate appearance for a game from
                  statsapi.
  lookup-games    Lookup games by a value.
  lookup-players  Lookup players by a value.
```
### `statsapi get`  
```sh
$ statsapi get --help
Usage: statsapi get [OPTIONS]

  get sends a request directly to the statsapi module with the parameters
  specified.

  Ex. statsapi get --module schedule --params '{"sportId": 1, "startDate":
  "4/1/2019", "endDate": "4/30/2019"}' --output ./output_dir

Options:
  --module TEXT  The module from statsapi.  [required]
  --params TEXT  The API parameters to pass to statsapi.
  --output PATH  Location for the output file.
  --help         Show this message and exit.
```
### `statsapi get-gamepks`  
```sh
$ statsapi get-gamepks --help
Usage: statsapi get-gamepks [OPTIONS]

  get-gamepks retrieves game pks for every day within the date range.

  Ex. statsapi get-gamepks --start 04/01/2019 --end 04/30/2019 --output
  ./output_dir

Options:
  --start TEXT        Start date to search after, inclusive.
  --end TEXT          End date to search before, inclusive.
  --sport-id INTEGER  Sport ID, MLB = 1
  --output PATH       Location for the output file.
  --help              Show this message and exit.
```
### `statsapi get-winprob`  
```sh
$ statsapi get-winprob --help
Usage: statsapi get-winprob [OPTIONS]

  get-winprob retrieves win probabilities for a game.

  Ex. statsapi get-winprob --game-pk 566180 --output ./output_dir

Options:
  --game-pk TEXT  Game PK for retrieving win probabilities.  [required]
  --output PATH   Location for the output file.
  --help          Show this message and exit.
```
### `statsapi lookup-players`
```sh
$ statsapi lookup-players --help
Usage: statsapi lookup-players [OPTIONS]

  lookup-players searches for players with the specified value in their
  profiles.

  Ex. statsapi lookup-players --value "Bryce Harper" --game-type R --season
  2019 --sport-id 1 --output ./output_dir

Options:
  --value TEXT        The value to search for in player profiles.  [required]
  --game-type TEXT    Game type.
  --season INTEGER    The season's year.
  --sport-id INTEGER  Sport ID, MLB = 1
  --output PATH       Location for the output file.
  --help              Show this message and exit.
```
### `statsapi lookup-games`  
```sh
$ statsapi lookup-games --help
Usage: statsapi lookup-games [OPTIONS]

  lookup-games searches for games with the specified value in their
  profiles.

  Ex. statsapi lookup-games --value "Indians" --start 4/1/2019 --end
  4/30/2020 --sport-id 1 --output ./output_dir

Options:
  --value TEXT        The value to search for in game profiles.  [required]
  --start TEXT        Start date to search after, inclusive.
  --end TEXT          End date to search before, inclusive.
  --sport-id INTEGER  Sport ID, MLB = 1
  --output PATH       Location for the output file.
  --help              Show this message and exit.
```

## Output Files
All output files are located in the specified output directory or if none is specified then the current directory. They all are JSON formatted and have the file name of <command_name>\_\<year>\_\<month>\_\<day>\_\<hour>\_\<minute>\_\<second>.json where the date time is when the file was created.

## Python wrapper for MLB StatsAPI Endpoints

An unassociated existing python wrapper for the MLB StatsAPI endpoints exists at the following repo and contains documentation of existing MLB StatsAPI endpoints.  

https://github.com/toddrob99/MLB-StatsAPI  
https://github.com/toddrob99/MLB-StatsAPI/wiki/Endpoints  
https://github.com/toddrob99/MLB-StatsAPI/blob/master/statsapi/endpoints.py  
