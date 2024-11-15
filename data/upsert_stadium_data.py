""" This python script is used to upsert all the data from the CSV into the 
"""

import csv
import os
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


def create_stadium(row: Dict[str, Any]):
    home_team = upsert("team", name=row["HomeTeam"])
    stadium_data = {"name": row["Name"], "home_team": home_team["name"]}
    headers = {"Authorization": f"Bearer {ADD_ACCESS_TOKEN}"}
    response = requests.post(
        f"{BASE_URL}/api/stadium/upsert", json=stadium_data, headers=headers
    )
    if response.status_code != 201:
        raise Exception(f"Failed to create stadium: {response.text}")


def parse_csv(csv_file_path: Path):
    with open(csv_file_path, "r", encoding="utf-8") as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in tqdm(csv_reader):
            create_stadium(row)


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
    stadium_file_path = stats_folder_path / "stadiums.csv"
    if not stadium_file_path.exists():
        raise Exception(
            "No stadiums.csv file found in this zip extraction. Please check your zip file"
        )

    parse_csv(stadium_file_path)
