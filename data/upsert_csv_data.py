""" This python script is used to upsert all the data from the CSV into the 
"""

import csv
import re
import sys
import zipfile
from argparse import ArgumentParser
from datetime import datetime
from os import listdir
from os.path import isfile, join
from pathlib import Path
from typing import Any, Dict
from tqdm import tqdm

import requests

parser = ArgumentParser()
parser.add_argument("zip_path")
parser.add_argument("base_url")

# Default to localhost
BASE_URL = "http://localhost:8000" 

def parse_date(date_str: str) -> str:
    try:
        date_obj = datetime.strptime(date_str, "%d/%m/%Y").strftime("%Y.%m.%d")
    except ValueError as e:
        date_obj = datetime.strptime(date_str, "%d/%m/%y").strftime("%Y.%m.%d")
    except Exception as e:
        raise Exception("Failed to parse the date ", date_str)
    finally:
        return date_obj


def parse_float(value: str) -> float:
    return float(value) if value else None


def get_or_create(model: str, **kwargs):
    """ Gets the specific model instance from the database if it exists. Else creates 
        it in the database

    Args:
        model (str): model type. Either 'season', 'team', 'referee' 

    Raises:
        Exception: Throws exception when model type is not valid or 
                   the database encounters some exception.

    Returns: The info to populate in the match model.
    """

    response = requests.get(f"{BASE_URL}/api/{model}/list", params=kwargs)
    if response.status_code == 200 and response.json():
        name = kwargs['name'] 

        # WARNING: This would fail if the anything other than a list is provided
        model_instance_set = set([instance['name'] for instance in response.json()])
        
        # Check if the request model name already exists in the database.
        # If it does, then return the model instance
        if name in model_instance_set:
            return response.json()
   
    # We can assume here that the model instance does not exist within 
    # the database. So we have to create it.
    response = requests.post(f"{BASE_URL}/api/{model}/add", json=kwargs)
    if response.status_code == 201:
        return response.json()
    else:
        raise Exception(f"Failed to create {model}: {response.text}")


    

def create_match(season_name, row: Dict[str, Any]):
    season = get_or_create("season", name=season_name)
    home_team = get_or_create("team", name=row["HomeTeam"])
    away_team = get_or_create("team", name=row["AwayTeam"])
    referee = get_or_create("referee", name=row["Referee"]) if row["Referee"] else None

    match_data = {
        "season_name": season["name"],
        "division": row["Div"],
        "match_date": parse_date(row["Date"]),
        "match_time": row["Time"],
        "home_team_name": home_team["name"],
        "away_team_name": away_team["name"],
        "referee_name": referee["name"] if referee else None,
        "full_time_home_goals": int(row["FTHG"]),
        "full_time_away_goals": int(row["FTAG"]),
        "full_time_result": row["FTR"],
        "half_time_home_goals": int(row["HTHG"]),
        "half_time_away_goals": int(row["HTAG"]),
        "half_time_result": row["HTR"],
        "home_shots": int(row["HS"]) if row["HS"] else None,
        "away_shots": int(row["AS"]) if row["AS"] else None,
        "home_shots_on_target": int(row["HST"]) if row["HST"] else None,
        "away_shots_on_target": int(row["AST"]) if row["AST"] else None,
        "home_fouls": int(row["HF"]) if row["HF"] else None,
        "away_fouls": int(row["AF"]) if row["AF"] else None,
        "home_corners": int(row["HC"]) if row["HC"] else None,
        "away_corners": int(row["AC"]) if row["AC"] else None,
        "home_yellow_cards": int(row["HY"]) if row["HY"] else None,
        "away_yellow_cards": int(row["AY"]) if row["AY"] else None,
        "home_red_cards": int(row["HR"]) if row["HR"] else None,
        "away_red_cards": int(row["AR"]) if row["AR"] else None,
        "bet365_home_win_odds": parse_float(row["B365H"]),
        "bet365_draw_odds": parse_float(row["B365D"]),
        "bet365_away_win_odds": parse_float(row["B365A"]),
        "bet_and_win_home_win_odds": parse_float(row["BWH"]),
        "bet_and_win_draw_odds": parse_float(row["BWD"]),
        "bet_and_win_away_win_odds": parse_float(row["BWA"]),
        "interwetten_home_win_odds": parse_float(row["IWH"]),
        "interwetten_draw_odds": parse_float(row["IWD"]),
        "interwetten_away_win_odds": parse_float(row["IWA"]),
        "pinnacle_home_win_odds": parse_float(row["PSH"]),
        "pinnacle_draw_odds": parse_float(row["PSD"]),
        "pinnacle_away_win_odds": parse_float(row["PSA"]),
        "william_hill_home_win_odds": parse_float(row["WHH"]),
        "william_hill_draw_odds": parse_float(row["WHD"]),
        "william_hill_away_win_odds": parse_float(row["WHA"]),
        "vc_bet_home_win_odds": parse_float(row["VCH"]),
        "vc_bet_draw_odds": parse_float(row["VCD"]),
        "vc_bet_away_win_odds": parse_float(row["VCA"]),
        "max_home_win_odds": parse_float(row["MaxH"]),
        "max_draw_odds": parse_float(row["MaxD"]),
        "max_away_win_odds": parse_float(row["MaxA"]),
        "avg_home_win_odds": parse_float(row["AvgH"]),
        "avg_draw_odds": parse_float(row["AvgD"]),
        "avg_away_win_odds": parse_float(row["AvgA"]),
        "bet365_over_2_5_odds": parse_float(row["B365>2.5"]),
        "bet365_under_2_5_odds": parse_float(row["B365<2.5"]),
        "pinnacle_over_2_5_odds": parse_float(row["P>2.5"]),
        "pinnacle_under_2_5_odds": parse_float(row["P<2.5"]),
        "max_over_2_5_odds": parse_float(row["Max>2.5"]),
        "max_under_2_5_odds": parse_float(row["Max<2.5"]),
        "avg_over_2_5_odds": parse_float(row["Avg>2.5"]),
        "avg_under_2_5_odds": parse_float(row["Avg<2.5"]),
        "asian_handicap_line": parse_float(row["AHh"]),
        "bet365_asian_handicap_home_odds": parse_float(row["B365AHH"]),
        "bet365_asian_handicap_away_odds": parse_float(row["B365AHA"]),
        "pinnacle_asian_handicap_home_odds": parse_float(row["PAHH"]),
        "pinnacle_asian_handicap_away_odds": parse_float(row["PAHA"]),
        "max_asian_handicap_home_odds": parse_float(row["MaxAHH"]),
        "max_asian_handicap_away_odds": parse_float(row["MaxAHA"]),
        "avg_asian_handicap_home_odds": parse_float(row["AvgAHH"]),
        "avg_asian_handicap_away_odds": parse_float(row["AvgAHA"]),
    }

    response = requests.post(f"{BASE_URL}/api/match/add", json=match_data)
    if response.status_code != 201:
        raise Exception(f"Failed to create match: {response.text}")


def parse_file_name_to_season(csv_file_name: str):
    """Parses the file name that we get into a season name.
        The file name being passed in is of the form : `prem_<season_year>_stats.csv`.
        We just need to extract the year and output `English Premier League <season/year> Season`

    Args:
        csv_file_name (str): only file name (without file extension) of the CSV file being parsed.
    """

    match = re.search(r'prem_(\d{2})_(\d{2})_stats', csv_file_name)
    if match:
        start_year = int(match.group(1))
        end_year = int(match.group(2))
        
        # Convert to full year format
        full_start_year = (2000 if start_year < 50 else 1900) + start_year
        
        # Format the season string
        season = f"{full_start_year}/{end_year:02d}"
        return f"English Premier League {season} Season"
    else:
        raise ValueError(f"Invalid filename format: {csv_file_name}")


def parse_csv(csv_file_path: Path):
    csv_file_name = csv_file_path.stem
    season_name = parse_file_name_to_season(csv_file_name)
    print(f"Parsing data for {season_name} ...")
    with open(csv_file_path, "r") as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in tqdm(csv_reader):
            create_match(season_name, row)


def is_alive(url) -> bool:
    response = requests.get(f"{url}/check")
    if response.status_code == 200 and response.json():
        return True
    else:
        return False


if __name__ == "__main__":
    args = parser.parse_args()

    zip_file_path = Path(args.zip_path)
    if not zip_file_path.exists():
        raise Exception("You need to specify a valid zip file path")

    if not is_alive(args.base_url):
        raise Exception("The server is not alive")
    BASE_URL = args.base_url

    # Make the stats folder where the zip file
    # will be extracted into
    stats_folder_path = Path("./stats")
    stats_folder_path.mkdir(exist_ok=True)

    # Unzip the zip file
    with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
        zip_ref.extractall(stats_folder_path)

    csv_files = [
        (stats_folder_path / f) for f in listdir(stats_folder_path) if (stats_folder_path / f).is_file()
    ]
    for csv_file in csv_files:
        parse_csv(csv_file)
        exit(0)
    
     