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
    "N. S. Barry": "Neale Barry",
    "P. A. Durkin": "Paul Durkin",
    "C. R. Wilkes": "Clive Wilkes",
    "R. Styles": "Rob Styles",
    "J. T. Winter": "Jeff Winter",
    "G. P. Barber": "Graham Barber",
    "G. Poll": "Graham Poll",
    "D. J. Gallagher": "Dermot Gallagher",
    "A. P. D'Urso": "Andy D'Urso",
    "P. Jones": "Phil Jones",
    "D. R. Elleray": "David Elleray",
    "S. W. Dunn": "Steve Dunn",
    "E. K. Wolstenholme": "Eddie Wolstenholme",
    "A. G. Wiley": "Alan Wiley",
    "B. Knight": "Barry Knight",
    "S. G. Bennett": "Steve Bennett",
    "U. D. Rennie": "Uriah Rennie",
    "M. L Dean": "Mike Dean",
    "D. Pugh": "David Pugh",
    "M. A. Riley": "Mike Riley",
    "M. R. Halsey": "Mark Halsey",
    "M. D. Messias": "Mark Messias",
    "C. J. Foy": "Chris Foy",
    "P. Dowd": "Phil Dowd",
    "Yates, N": "Neale Barry",  # If Yates is a variant of N. S. Barry
    "Wiley, A. G.": "Alan Wiley",
    "Elleray, D. R.": "David Elleray",
    "Winter, J. T.": "Jeff Winter",
    "Wolstenholme, E. K.": "Eddie Wolstenholme",
    "Dunn, S. W.": "Steve Dunn",
    "Knight, B.": "Barry Knight",
    "Rennie, U. D.": "Uriah Rennie",
    "Dean, M. L": "Mike Dean",
    "Poll, G.": "Graham Poll",
    "Halsey, M. R.": "Mark Halsey",
    "Dowd, P.": "Phil Dowd",
    "Jones, P.": "Phil Jones",
    "Styles, R.": "Rob Styles",
    "Gallagher, D. J.": "Dermot Gallagher",
    "D'Urso, A. P.": "Andy D'Urso",
    "Durkin, P. A.": "Paul Durkin",
    "Barber, G. P.": "Graham Barber",
    "Wilkes, C. R.": "Clive Wilkes",
    "Foy, C. J.": "Chris Foy",
    "Messias, M. D.": "Mark Messias",
    "D Gallagh": "Dermot Gallagher",
    "D Gallaghe": "Dermot Gallagher",
    "R Martin": "Ross Martin",
    "T Bramall": "Thomas Bramall",
    "D Bond": "Darren Bond",
    "J Smith": "Joshua Smith",
    "N. S. Barry": "Neil Barry",
    "P. A. Durkin": "Paul Durkin",
    "C. R. Wilkes": "Clive Wilkes",
    "R. Styles": "Rob Styles",
    "J. T. Winter": "Jeff Winter",
    "G. P. Barber": "Graham Barber",
    "G. Poll": "Graham Poll",
    "D. J. Gallagher": "Dermot Gallagher",
    "A. P. D'Urso": "Andy D'Urso",
    "A.G. Wiley": "Alan Wiley",
    "P. Jones": "Phil Jones",
    "D. R. Elleray": "David Elleray",
    "S. W. Dunn": "Steve Dunn",
    "E. K. Wolstenholme": "Eddie Wolstenholme",
    "A. G. Wiley": "Alan Wiley",
    "B. Knight": "Barry Knight",
    "S. G. Bennett": "Steve Bennett",
    "U. D. Rennie": "Uriah Rennie",
    "M. L Dean": "Mike Dean",
    "M. L. Dean": "Mike Dean",
    "M. A. Riley": "Mike Riley",
    "M. R. Halsey": "Mark Halsey",
    "M. D. Messias": "Mark Messias",
    "P. Dowd": "Phil Dowd",
    "C. J. Foy": "Chris Foy",
    "D. Pugh": "David Pugh",
    "Yates, N": "Neale Barry",
    "A Moss": "Anthony Moss",
    "Wiley, A. G.": "Alan Wiley",
    "Elleray, D. R.": "David Elleray",
    "Winter, J. T.": "Jeff Winter",
    "J.T. Winter": "Jeff Winter",
    "Wolstenholme, E. K.": "Eddie Wolstenholme",
    "Dunn, S. W.": "Steve Dunn",
    "Knight, B.": "Barry Knight",
    "Riley, M. A.": "Mike Riley",
    "Rennie, U. D.": "Uriah Rennie",
    "Durkin, P. A.": "Paul Durkin",
    "P.A. Durkin": "Paul Durkin",
    "l Mason": "Lee Mason",
    "Styles, R": "Rob Styles",
    "Barber, G. P.": "Graham Barber",
    "D'Urso, A. P.": "Andy D'Urso",
    "Wilkes, C. R.": "Clive Wilkes",
    "Bennett, S. G.": "Steve Bennett",
    "Barry, N. S.": "Neil Barry",
    "Halsey, M. R.": "Mark Halsey",
    "Jones, P.": "Phil Jones",
    "Poll, G.": "Graham Poll",
    "Pugh, D.": "David Pugh",
    "Styles, R.": "Rob Styles",
    "Gallagher, D. J.": "Dermot Gallagher",
    "Dean, M. L.": "Mike Dean",
    "Messias, M. D.": "Mark Messias",
    "Foy, C. J.": "Chris Foy",
    "Durkin, P.": "Paul Durkin",
}


def clean_csv(csv_file_path: Path) -> str:
    cleaned_rows = []
    csv_file_name = csv_file_path.name
    with open(csv_file_path, "r", encoding="utf-8") as csvfile:
        csv_reader = csv.DictReader(csvfile)
        fieldnames = csv_reader.fieldnames

        # Process each row, replace referee names
        for row in tqdm(csv_reader, desc=f"Cleaning {csv_file_path.name}"):

            # Not all CSVs have a referee column, so we need to check if it exists
            referee_name = row.get("Referee")
            if referee_name is not None:
                referee_name = referee_name.strip()

            home_team_name = row["HomeTeam"].strip()
            away_team_name = row["AwayTeam"].strip()
            if csv_file_name == "prem_01_02_stats.csv":
                print(referee_name, home_team_name, away_team_name)

            if referee_name is not None and referee_name in REFEREE_NAME_CLEANING:
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
