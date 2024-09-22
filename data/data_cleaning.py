import csv
import os
import zipfile
from argparse import ArgumentParser
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Dict

from tqdm import tqdm

parser = ArgumentParser()
parser.add_argument(
    "zip_path", help="The path to the zip file to extract the CSVs from"
)

TEAM_NAME_CLEANING = {
    "Man United": "Manchester United",
    "Man City": "Manchester City",
    "Tottenham": "Tottenham Hotspur",
    "Nott'm Forest": "Nottingham Forest",
}

REFEREE_NAME_CLEANING = {
    "M Oliver": "Michael Oliver",
    "M Dean": "Mike Dean",
    "K Friend": "Kevin Friend",
    "G Scott": "Graham Scott",
    "J Moss": "Jonathan Moss",
    "C Pawson": "Craig Pawson",
    "C Kavanagh": "Chris Kavanagh",
    "A Marriner": "Andre Marriner",
    "M Atkinson": "Martin Atkinson",
    "A Taylor": "Anthony Taylor",
    "L Mason": "Lee Mason",
    "S Attwell": "Stuart Attwell",
    "D Coote": "David Coote",
    "O Langford": "Oliver Langford",
    "P Tierney": "Paul Tierney",
    "A Madley": "Andy Madley",
    "P Bankes": "Peter Bankes",
    "S Hooper": "Simon Hooper",
    "T Robinson": "Tim Robinson",
    "R Jones": "Robert Jones",
    "S Scott": "Simon Scott",
    "D England": "Darren England",
    "M Clattenburg": "Mark Clattenburg",
    "A Wiley": "Alan Wiley",
    "M Halsey": "Mark Halsey",
    "S Bennett": "Steve Bennett",
    "C Foy": "Chris Foy",
    "P Dowd": "Phil Dowd",
    "M Jones": "Mike Jones",
    "L Probert": "Lee Probert",
    "P Walton": "Peter Walton",
    "H Webb": "Howard Webb",
    "St Bennett": "Steve Bennett",
    "Mn Atkinson": "Martin Atkinson",
    "R Madley": "Robert Madley",
    "R East": "Roger East",
    "N Swarbrick": "Neil Swarbrick",
    "J Gillett": "Jarred Gillett",
    "M Salisbury": "Michael Salisbury",
    "J Brooks": "John Brooks",
    "T Harrington": "Tony Harrington",
    "M Riley": "Mike Riley",
    "R Styles": "Rob Styles",
    "K Stroud": "Keith Stroud",
    "S Tanner": "Scott Tanner",
    "U Rennie": "Uriah Rennie",
    "M Messias": "Matt Messias",
    "D Gallagher": "Dermot Gallagher",
    "G Poll": "Graham Poll",
    "B Knight": "Barry Knight",
    "N Barry": "Neale Barry",
    "A D'Urso": "Andy D'Urso",
    "S Dunn": "Steve Dunn",
    "P Crossley": "Paul Crossley",
    "R Beeby": "Ray Beeby",
    "D Elleray": "David Elleray",
    "G Barber": "Graham Barber",
    "P Durkin": "Paul Durkin",
    "J Winter": "Jeff Winter",
    "C Wilkes": "Clive Wilkes",
    "D Pugh": "David Pugh",
    "E Wolstenholme": "Eddie Wolstenholme",
    "Rob Harris": "Robert Harris",
    "Steve Lodge": "Steve Lodge",
    "Peter Jones": "Peter Jones",
    "Andy Hall": "Andy Hall",
    "David Ellaray": "David Elleray",
    "F Taylor": "Frank Taylor",
    "Ian Harris": "Ian Harris",
    "Paul Taylor": "Paul Taylor",
    "Roy Burton": "Roy Burton",
    "Clive Wilkes": "Clive Wilkes",
    "Andy Yates": "Andy Yates",
    "I Williamson": "Ian Williamson",
    "S Barrott": "Sam Barrott",
    "R Welch": "Rob Welch",
    "S Allison": "Simon Allison",
    "L Smith": "Lee Smith",
    "S Singh": "Sunny Singh",
    "M Donohue": "Matt Donohue",
}


def clean_csv(csv_file_path: Path) -> str:
    cleaned_rows = []

    with open(csv_file_path, "r", encoding="utf-8") as csvfile:
        csv_reader = csv.DictReader(csvfile)
        fieldnames = csv_reader.fieldnames
        if "Referee" not in fieldnames:
            print(f"Skipping {csv_file_path}, no 'Referee' column found.")
            return  # Skip if no 'Referee' column

        # Process each row, replace referee names
        for row in tqdm(csv_reader, desc=f"Cleaning {csv_file_path.name}"):
            referee_name = row["Referee"].strip()
            home_team_name = row["HomeTeam"].strip()
            away_team_name = row["AwayTeam"].strip()
            if referee_name in REFEREE_NAME_CLEANING:
                row["Referee"] = REFEREE_NAME_CLEANING[referee_name]
            if home_team_name in TEAM_NAME_CLEANING:
                row["HomeTeam"] = TEAM_NAME_CLEANING[home_team_name]
            if away_team_name in TEAM_NAME_CLEANING:
                row["AwayTeam"] = TEAM_NAME_CLEANING[away_team_name]
            cleaned_rows.append(row)

    # Write the cleaned data back to the file
    with open(csv_file_path, "w", newline="", encoding="utf-8") as csvfile:
        csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csv_writer.writeheader()
        csv_writer.writerows(cleaned_rows)


if __name__ == "__main__":
    args = parser.parse_args()

    zip_file_path = Path(args.zip_path)
    if not zip_file_path.exists():
        raise Exception("You need to specify a valid zip file path")

    # Make a temporary directory to extract the zip file
    with TemporaryDirectory() as tmpdirname:
        stats_folder_path = Path(tmpdirname)
        stats_folder_path.mkdir(exist_ok=True)

        # Unzip the zip file
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

        print("Cleaning the CSV files ...")
        for csv_file in csv_files:
            clean_csv(csv_file)

        # Create a new zip file with the cleaned CSVs
        cleaned_zip_path = zip_file_path.with_stem(f"{zip_file_path.stem}_cleaned")
        print(f"Saving cleaned CSV files to {cleaned_zip_path} ...")
        with zipfile.ZipFile(cleaned_zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for csv_file in csv_files:
                zipf.write(csv_file, arcname=csv_file.name)

        print("Cleaning complete ...")
