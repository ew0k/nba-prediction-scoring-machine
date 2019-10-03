import json
import os
import http.client

def get_standings():
    conn = http.client.HTTPSConnection("api.sportradar.us")

    conn.request("GET", "/nba/trial/v7/en/seasons/2018/REG/standings.json?api_key=" + os.environ.get('SPORTRADAR_KEY'))

    res = conn.getresponse()
    data = res.read()
    return data

def parse_json(json_string):
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
    return west_conference_standings, east_conference_standings

def main():
    nba_data = get_standings()
    west_conference_standings, east_conference_standings = parse_json(json.loads(nba_data))

    print("West Standings")
    for standing in range(1, 15+1):
        team_name = west_conference_standings[standing]
        print(team_name + ": " + str(standing))

    print()
    print("East Standings")
    for standing in range(1, 15+1):
        team_name = east_conference_standings[standing]
        print(team_name + ": " + str(standing))

main()