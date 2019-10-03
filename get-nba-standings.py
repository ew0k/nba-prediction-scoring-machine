import json
import os

standings_file_name = "nba-standings.json"
sportradar_key = os.environ.get('SPORTRADAR_KEY')
os.system("curl -X GET \"https://api.sportradar.us/nba/trial/v7/en/seasons/2018/REG/standings.json?api_key={" + sportradar_key + "}\" > " + standings_file_name)

standings_file = open(standings_file_name, "r")

json_string = json.load(standings_file)

west_conference_standings = {}
east_conference_standings = {}

for conference in json_string["conferences"]:
    for division in conference["divisions"]:
        for team in division["teams"]:
            team_name = team["name"]
            team_conference_standing = team["calc_rank"]["conf_rank"]
            if conference["name"].lower() == "western conference": 
                west_conference_standings[team_conference_standing] = team_name
            if conference["name"].lower() == "eastern conference":
                east_conference_standings[team_conference_standing] = team_name

print("West Standings")
for standing in range(1, 15+1):
    team_name = west_conference_standings[standing]
    print(team_name + ": " + str(standing))

print()
print("East Standings")
for standing in range(1, 15+1):
    team_name = east_conference_standings[standing]
    print(team_name + ": " + str(standing))

