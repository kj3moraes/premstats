""" This python script is used to upsert all the data from the CSV into the 
"""

import csv
import os
import re
import time
import zipfile
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict

import requests
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential
from tqdm import tqdm

parser = ArgumentParser()
parser.add_argument(
    "zip_path", help="The path to the zip file to extract the CSVs from"
)
parser.add_argument("base_url", help="The URL for the server")
parser.add_argument(
    "--no-extract",
    action="store_true",
    help="Flag to not extract the zipfile and use the stats/ directory instead.",
)

# Default to localhost
BASE_URL = "http://localhost:8000"
load_dotenv()
ADD_ACCESS_TOKEN = os.getenv("ADD_ACCESS_TOKEN")


def parse_float(value: str) -> float:
    return float(value) if value else None


@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=4, max=10),
)
def upsert(model: str, **kwargs) -> Dict[str, Any]:
    """
    Updates the specific model instance from the database if it exists. Else creates
    it in the database with retry logic to handle race conditions.

    Args:
        model (str): model type. Either 'season', 'team', 'referee'
    Raises:
        Exception: Throws exception when model type is not valid or
                   the database encounters some exception.
    Returns:
        Dict[str, Any]: The info to populate in the match model.
    """
    try:
        # Upsert the model straight away
        headers = {"Authorization": f"Bearer {ADD_ACCESS_TOKEN}"}
        response = requests.post(
            f"{BASE_URL}/api/{model}/upsert", json=kwargs, headers=headers
        )
        if response.status_code == 201:
            return response.json()
        else:
            raise Exception(f"Failed to upsert {model}: {response.text}")
    except:
        raise Exception(f"Failed to create {model}: {response.text}")


def create_match(season_name, row: Dict[str, Any]):
    season = upsert("season", name=season_name)
    home_team = upsert("team", name=row["HomeTeam"])
    away_team = upsert("team", name=row["AwayTeam"])
    if "Referee" in row:
        referee = upsert("referee", name=row["Referee"]) if row["Referee"] else None
    else:
        referee = None

    match_data = {
        "season_name": season["name"],
        "division": row["Div"],
        "match_date": row["Date"],
        "match_time": row["Time"] if "Time" in row else None,
        "home_team_name": home_team["name"],
        "away_team_name": away_team["name"],
        "referee_name": referee["name"] if referee else None,
        "full_time_home_goals": int(row["FTHG"]),
        "full_time_away_goals": int(row["FTAG"]),
        "full_time_result": row["FTR"],
        "half_time_home_goals": int(row["HTHG"]) if "HTHG" in row else None,
        "half_time_away_goals": int(row["HTAG"]) if "HTHG" in row else None,
        "half_time_result": row["HTR"] if "HTR" in row else None,
        "home_shots": int(row["HS"]) if "HS" in row and row["HS"] else None,
        "away_shots": int(row["AS"]) if "AS" in row and row["AS"] else None,
        "home_shots_on_target": (
            int(row["HST"]) if "HST" in row and row["HST"] else None
        ),
        "away_shots_on_target": (
            int(row["AST"]) if "AST" in row and row["AST"] else None
        ),
        "home_fouls": int(row["HF"]) if "HF" in row and row["HF"] else None,
        "away_fouls": int(row["AF"]) if "AF" in row and row["AF"] else None,
        "home_corners": int(row["HC"]) if "HC" in row and row["HC"] else None,
        "away_corners": int(row["AC"]) if "AC" in row and row["AC"] else None,
        "home_yellow_cards": int(row["HY"]) if "HY" in row and row["HY"] else None,
        "away_yellow_cards": int(row["AY"]) if "AY" in row and row["AY"] else None,
        "home_red_cards": int(row["HR"]) if "HR" in row and row["HR"] else None,
        "away_red_cards": int(row["AR"]) if "AR" in row and row["AR"] else None,
        "bet365_home_win_odds": parse_float(row["B365H"]) if "B365H" in row else None,
        "bet365_draw_odds": parse_float(row["B365D"]) if "B365D" in row else None,
        "bet365_away_win_odds": parse_float(row["B365A"]) if "B365A" in row else None,
        "bet_and_win_home_win_odds": parse_float(row["BWH"]) if "BWH" in row else None,
        "bet_and_win_draw_odds": parse_float(row["BWD"]) if "BWD" in row else None,
        "bet_and_win_away_win_odds": parse_float(row["BWA"]) if "BWA" in row else None,
        "interwetten_home_win_odds": parse_float(row["IWH"]) if "IWH" in row else None,
        "interwetten_draw_odds": parse_float(row["IWD"]) if "IWD" in row else None,
        "interwetten_away_win_odds": parse_float(row["IWA"]) if "IWA" in row else None,
        "pinnacle_home_win_odds": parse_float(row["PSH"]) if "PSH" in row else None,
        "pinnacle_draw_odds": parse_float(row["PSD"]) if "PSD" in row else None,
        "pinnacle_away_win_odds": parse_float(row["PSA"]) if "PSA" in row else None,
        "william_hill_home_win_odds": parse_float(row["WHH"]) if "WHH" in row else None,
        "william_hill_draw_odds": parse_float(row["WHD"]) if "WHD" in row else None,
        "william_hill_away_win_odds": parse_float(row["WHA"]) if "WHA" in row else None,
        "vc_bet_home_win_odds": parse_float(row["VCH"]) if "VCH" in row else None,
        "vc_bet_draw_odds": parse_float(row["VCD"]) if "VCD" in row else None,
        "vc_bet_away_win_odds": parse_float(row["VCA"]) if "VCA" in row else None,
        "max_home_win_odds": parse_float(row["MaxH"]) if "MaxH" in row else None,
        "max_draw_odds": parse_float(row["MaxD"]) if "MaxD" in row else None,
        "max_away_win_odds": parse_float(row["MaxA"]) if "MaxA" in row else None,
        "avg_home_win_odds": parse_float(row["AvgH"]) if "AvgH" in row else None,
        "avg_draw_odds": parse_float(row["AvgD"]) if "AvgD" in row else None,
        "avg_away_win_odds": parse_float(row["AvgA"]) if "AvgA" in row else None,
        "bet365_over_2_5_odds": (
            parse_float(row["B365>2.5"]) if "B365>2.5" in row else None
        ),
        "bet365_under_2_5_odds": (
            parse_float(row["B365<2.5"]) if "B365<2.5" in row else None
        ),
        "pinnacle_over_2_5_odds": parse_float(row["P>2.5"]) if "P>2.5" in row else None,
        "pinnacle_under_2_5_odds": (
            parse_float(row["P<2.5"]) if "P<2.5" in row else None
        ),
        "max_over_2_5_odds": parse_float(row["Max>2.5"]) if "Max>2.5" in row else None,
        "max_under_2_5_odds": parse_float(row["Max<2.5"]) if "Max<2.5" in row else None,
        "avg_over_2_5_odds": parse_float(row["Avg>2.5"]) if "Avg>2.5" in row else None,
        "avg_under_2_5_odds": parse_float(row["Avg<2.5"]) if "Avg<2.5" in row else None,
        "asian_handicap_line": parse_float(row["AHh"]) if "AHh" in row else None,
        "bet365_asian_handicap_home_odds": (
            parse_float(row["B365AHH"]) if "B365AHH" in row else None
        ),
        "bet365_asian_handicap_away_odds": (
            parse_float(row["B365AHA"]) if "B365AHA" in row else None
        ),
        "pinnacle_asian_handicap_home_odds": (
            parse_float(row["PAHH"]) if "PAHH" in row else None
        ),
        "pinnacle_asian_handicap_away_odds": (
            parse_float(row["PAHA"]) if "PAHA" in row else None
        ),
        "max_asian_handicap_home_odds": (
            parse_float(row["MaxAHH"]) if "MaxAHH" in row else None
        ),
        "max_asian_handicap_away_odds": (
            parse_float(row["MaxAHA"]) if "MaxAHA" in row else None
        ),
        "avg_asian_handicap_home_odds": (
            parse_float(row["AvgAHH"]) if "AvgAHH" in row else None
        ),
        "avg_asian_handicap_away_odds": (
            parse_float(row["AvgAHA"]) if "AvgAHA" in row else None
        ),
    }

    headers = {"Authorization": f"Bearer {ADD_ACCESS_TOKEN}"}
    response = requests.post(
        f"{BASE_URL}/api/match/upsert", json=match_data, headers=headers
    )
    if response.status_code != 201:
        raise Exception(f"Failed to create match: {response.text}")


def parse_file_name_to_season(csv_file_name: str):
    """Parses the file name that we get into a season name.
        The file name being passed in is of the form : `prem_<season_year>_stats.csv`.
        We just need to extract the year and output `English Premier League <season/year> Season`

    Args:
        csv_file_name (str): only file name (without file extension) of the CSV file being parsed.
    """

    match = re.search(r"prem_(\d{2})_(\d{2})_stats", csv_file_name)
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
    with open(csv_file_path, "r", encoding="utf-8") as csvfile:
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
    if not args.no_extract:
        print("Extracting the zip file ...")
        with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
            zip_ref.extractall(stats_folder_path)

    # List all the csv files in the extracted directory.
    csv_files = [
        (stats_folder_path / f)
        for f in os.listdir(stats_folder_path)
        if (
            (stats_folder_path / f).is_file()
            and (stats_folder_path / f).suffix == ".csv"
        )
    ]
    for csv_file in csv_files:
        parse_csv(csv_file)
