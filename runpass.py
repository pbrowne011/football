'''
runpass.py
A script that calculates the conditional probabilities of a run
or pass play, depending on the previous play
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

# name of dictionary is previous play type
# dictionary entries are the play type that followed
run = {
    "run": 0,
    "throw": 0
}

throw = {
    "run": 0,
    "throw": 0
}

for week in range(1, 17):
    try:
        # Drive data and results
        prev_play = None
        api_response = api_plays_instance.get_plays(year, team=team, offense=team, week=week)
        for play in api_response:
            # set current play
            if "pass" in play.play_type.lower():
                curr_play = "throw"
            elif "rush" in play.play_type.lower():
                curr_play = "run"
            else:
                curr_play = None

            # check previous play
            if curr_play:
                if prev_play == "throw":
                    throw[curr_play] += 1
                elif prev_play == "run":
                    run[curr_play] += 1
        
            prev_play = curr_play

    except ApiException as e:
        print("Exception when calling DrivesApi->get_drives: %s\n" % e)
        break

print("The previous play was a pass")
print("Number of rushes after a pass:", throw["run"])
print("Number of passes after a pass:", throw["throw"])
print()
print("The previous play was a rush")
print("Number of rushes after a rush:", run["run"])
print("Number of passes after a rush:", run["throw"])