# CLI Tool for MLB's StatsAPI

`statsapi` is a standardized tool that can be used to download data from
MLB's StatsAPI and other data sources directly from the CLI. Some commands append additional data to the MLB StatsAPI responses. It was developed using a python package, [Click](https://click.palletsprojects.com/en/7.x/).


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

#### `statsapi --help`
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
  get-lahman      Get data from Lahman's baseball database.
  get-pitches     Get pitches for a game from statsapi.
  get-re24        Get play by play of a specific game with RE24 for each play.
  get-weather     Get schedule with weather data for future games from
                  statsapi.
  get-winprob     Get win probabilities per plate appearance for a game from
                  statsapi.
  lookup-games    Lookup games by a value.
  lookup-players  Lookup players by a value.
  lookup-re24     Lookup RE24 values by year.
```

### Standard StatsAPI Commands

The following commands can be used to download full or subsets of data using standard StatsAPI endpoints.

#### `statsapi get`  
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

#### `statsapi get-gamepks`  
```sh
$ statsapi get-gamepks --help
Usage: statsapi get-gamepks [OPTIONS]

  get-gamepks retrieves game pks for every day within the date range.

  Ex. statsapi get-gamepks --start 04/01/2019 --end 04/30/2019 --sport-id 1
  --output ./output_dir

Options:
  --start TEXT        Start date to search after, inclusive.
  --end TEXT          End date to search before, inclusive.
  --sport-id INTEGER  Sport ID, MLB = 1
  --output PATH       Location for the output file.
  --help              Show this message and exit.
```

#### `statsapi get-winprob`  
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

### Lookup StatsAPI Commands

The following commands can be used to lookup data by filtering based on key values.

#### `statsapi lookup-players`
```sh
$ statsapi lookup-players --help
Usage: statsapi lookup-players [OPTIONS]

  lookup-players searches for players with the specified value in their
  profiles.

  Ex. statsapi lookup-players --value "Bryce Harper" --game-type R --season
  2019 --sport-id 1 --output ./output_dir

Options:
  --value TEXT        The value to search for in player profiles.  [required]
  --game-type TEXT    Game type.  [default: R]
  --season INTEGER    The season's year.  [default: 2020]
  --sport-id INTEGER  Sport ID, MLB = 1  [default: 1]
  --output PATH       Location for the output file.
  --help              Show this message and exit.
```

#### `statsapi lookup-games`  
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

#### `statsapi lookup-re24`  
```sh
$ statsapi lookup-re24 --help
Usage: statsapi lookup-re24 [OPTIONS]

  lookup-re24 searches for RE24 values based on specified year. Only values
  starting in 2001 are available.

  Ex. statsapi lookup-re24 --year 2001 --output ./output_dir

Options:
  --year TEXT    Year for looking up RE24 values.  [required]
  --output PATH  Location for the output file.
  --help         Show this message and exit.
```

### Add-on StatsAPI Commands

The following commands add additional data to the standard StatsAPI endpoint responses or retrieve data not associated with the standard StatsAPI endpoints.

#### `statsapi get-re24`  
```sh
$ statsapi get-re24 --help
Usage: statsapi get-re24 [OPTIONS]

  get-re24 play by play for a single game with calculated RE24. Play by play
  data only exists starting in 2001, due to data limitations this command
  only works starting in 2003.

  Ex. statsapi get-re24 --game-pk 566180 --output ./output_dir

Options:
  --game-pk TEXT  Game PK for calculating RE24.  [required]
  --output PATH   Location for the output file.
  --help          Show this message and exit.
```

#### `statsapi get-pitches`  
```sh
$ statsapi get-pitches --help
Usage: statsapi get-pitches [OPTIONS]

  get-pitches retrieves pitches for a specified game PK. Play by play data
  only exists starting in 2001, due to data limitations this command only
  works starting in 2003.

  Ex. statsapi get-pitches --game-pk 566180 --output ./output_dir

Options:
  --game-pk TEXT  Game PK for retrieving pitches.  [required]
  --output PATH   Location for the output file.
  --help          Show this message and exit.
```

#### `statsapi get-lahman`  
```sh
$ statsapi get-lahman --help
Usage: statsapi get-lahman [OPTIONS]

  get-lahman retrieves data from Lahman's baseball database. Source:
  http://www.seanlahman.com/baseball-archive/statistics/.

  Ex. statsapi get-lahman --table Batting --output ./output_dir

Options:
  --table TEXT   Table to retrieve from Lahman's baseball database.
                 [required]
  --output PATH  Location for the output file.
  --help         Show this message and exit.
```

#### `statsapi get-weather`  
```sh
$ statsapi get-weather --help
Usage: statsapi get-weather [OPTIONS]

  get-weather retrieves schedule with weather data for games within the next
  16 days from statsapi. Requires a free Weatherbit API Key.

  Ex. statsapi get-weather --start 04/01/2020 --end 04/15/2020 --output
  ./output_dir

Options:
  --start TEXT        Start date to search after, inclusive.
  --end TEXT          End date to search before, inclusive.
  --sport-id INTEGER  Sport ID, MLB = 1
  --output PATH       Location for the output file.
  --help              Show this message and exit.
```

## Output Files
All output files are located in the specified output directory or if none is specified then the current directory. They all are JSON formatted and have the file name of `<command_name>_<year>_<month>_<day>_<hour>_<minute>_<second>.json` where the date time is when the file was created.

## Configurations

Create and update a `config.json` file to add configurations for statsapi. The `config-template.json` file contains all of the configuration options:

```json
{
  "weatherbit_api_key": "<insert free API key to enable weather data>"
}
```


## Data Sources

* MLB StatsAPI: https://statsapi.mlb.com/api/  
* Baseball Prospectus RE24 values by year: https://legacy.baseballprospectus.com/sortable/index.php?cid=2800999  
* Lahman's Baseball Database: http://www.seanlahman.com/baseball-archive/statistics/  
* Weatherbit API: https://www.weatherbit.io/api  

All data from MLB's StatsAPI has `Copyright 2020 MLB Advanced Media, L.P.  Use of any content on this page acknowledges agreement to the terms posted here http://gdx.mlb.com/components/copyright.txt"`

## Python wrapper for MLB StatsAPI Endpoints

An unassociated existing python wrapper for the MLB StatsAPI endpoints exists at the following repo and contains documentation of existing MLB StatsAPI endpoints.  

https://github.com/toddrob99/MLB-StatsAPI  
https://github.com/toddrob99/MLB-StatsAPI/wiki/Endpoints  
https://github.com/toddrob99/MLB-StatsAPI/blob/master/statsapi/endpoints.py  
