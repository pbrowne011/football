'''
firstplayofdrive.py
A script that determines the run-pass split on the first drive of the
series.
'''

import cfbd
from cfbd.rest import ApiException
import credentials

api_key = credentials.CFBD_API_KEY
configuration = cfbd.Configuration()
configuration.api_key['Authorization'] = api_key
configuration.api_key_prefix['Authorization'] = 'Bearer'

api_config = cfbd.ApiClient(configuration)

api_plays_instance = cfbd.PlaysApi(api_config)
year = 2023
team = "Notre Dame"

first_play = {
    "run": 0,
    "pass": 0,
    "penalty": 0
}

penalty_quarters = [0, 0, 0, 0, 0]

for week in range(1, 17):
    try:
        # Drive data and results
        api_response = api_plays_instance.get_plays(year, team=team, week=week)
        for play in api_response:
            # this disregards drives that start with a timeout, end of period,
            # sack, fumble - could be improved to track these catetories
            if play.offense == team and play.play_number == 2:
                if "pass" in play.play_type.lower():
                    first_play["pass"] += 1
                elif "rush" in play.play_type.lower():
                    first_play["run"] += 1
                elif "penalty" in play.play_type.lower():
                    first_play["penalty"] += 1
                    penalty_quarters[play.period] += 1
                else:
                    pass
                    # print(play.play_type)

    except ApiException as e:
        print("Exception when calling DrivesApi->get_drives: %s\n" % e)
        break

print("What's the run-pass breakdown of the first play of an ND drive?")
print("Number of rushes on first play:", first_play["run"])
print("Number of passes on first play:", first_play["pass"])
print("Number of pentalties on first play:", first_play["penalty"])
print()
print("What was the breakdown of the quarters of these penalties?")
for i in range(1, 5):
    print(f"Q{i}:", penalty_quarters[i])