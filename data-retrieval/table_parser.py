import os
import csv
import pandas as pd
from bs4 import BeautifulSoup
from webscraper.webscraper.helpers import league_code_defs, color_code_defs

# Open file to store data
f = open("./data/table_data.csv", "w", encoding="utf-8", newline='')
writer = csv.writer(f)

# Write data headers
column_headers = ["Country", "League", "Year", "Club", "Matchday", "Position", "Fate", "Matches", "Wins", "Draws", "Losses", "Goals For", "Goals Against", "Goal Differential", "Points", "Final Table"]
writer.writerow(column_headers)

# Set directory and loop through all files therein
directory = "./webscraper/webpages"
filename = os.listdir(directory)[0]

bgcs = []
bgcs_info = []

for filename in os.listdir(directory):
    # Print which file is being processed to show progress
    print("Processing:", filename)

    # Get information from filename
    fn_data = filename[:-5].split("-")
    year = fn_data[2]
    league_code = fn_data[1]
    country = league_code_defs[league_code]["country"]
    league = league_code_defs[league_code]["league"]
    matchday = int(fn_data[3][2:])

    # Create path and try to access file
    path = os.path.join(directory, filename)
    if os.path.isfile(path):

        # Get info from table
        with open(path, "r", encoding="utf-8") as fp:
            soup = BeautifulSoup(fp, 'html.parser')
            table = soup.find("table", {"class": ["items"]}).find("tbody")
            rows = table.find_all("tr")
            for row in rows:
                cells = row.find_all("td")
                position = int(cells[0].text)
                if cells[0].has_attr("style"):
                    bgc = cells[0]["style"].split("#")[1]
                else:
                    bgc = None
                fate = color_code_defs[bgc] if bgc in color_code_defs else "Mid Table"
                club = cells[1].find("a")["title"]
                matches = int(cells[3].text)
                wins = int(cells[4].text)
                draws = int(cells[5].text)
                losses = int(cells[6].text)
                goals = cells[7].text.split(":")
                goals_for = int(goals[0])
                goals_against = int(goals[1])
                goal_diff = int(cells[8].text)
                points = int(cells[9].text)

                if country == "Germany" and matchday == 34:
                    final_table = True
                elif matchday == 38:
                    final_table = True
                else:
                    final_table = False

                # Create list of data with above variables, write as row to CSV
                data_row = [country, league, year, club, matchday, position, fate, matches, wins, draws, losses, goals_for, goals_against, goal_diff, points, final_table]
                writer.writerow(data_row)

# Close CSV
f.close()

df = pd.read_csv('./data/table_data.csv')

