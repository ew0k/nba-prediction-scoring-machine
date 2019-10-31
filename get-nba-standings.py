import json
import os
import http.client


def get_sportradar_key():
    try:
        sportradar_key_file = open("sportradar_key.dontpush")
    except:
        print("Cannot find sportradar_key.dontpush file")
        exit(1)
    
    sportradar_key = sportradar_key_file.readline().strip()
    if len(sportradar_key) == 0:
        print("No key in sportradar_key.dontpush file")
        exit(1)

    sportradar_key_file.close()
    return sportradar_key


def get_standings(sportradar_key):
    conn = http.client.HTTPSConnection("api.sportradar.us")
    conn.request("GET", "/nba/trial/v7/en/seasons/2019/REG/standings.json?api_key=" + sportradar_key)
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
                    west_conference_standings[team_name] = team_conference_standing
                if conference["name"].lower() == "eastern conference":
                    east_conference_standings[team_name] = team_conference_standing
    return west_conference_standings, east_conference_standings


def print_standings(west_conference_standings, east_conference_standings):
    print("West Standings")
    for key, value in sorted(west_conference_standings.items(), key=lambda item: item[1]):
        print("%s: %s" % (key, value))

    print()
    print("East Standings")
    for key, value in sorted(east_conference_standings.items(), key=lambda item: item[1]):
        print("%s: %s" % (key, value))


def main():
    sportradar_key = get_sportradar_key()
    nba_data = get_standings(sportradar_key)
    west_conference_standings, east_conference_standings = parse_json(json.loads(nba_data))
    print_standings(west_conference_standings, east_conference_standings)

main()
