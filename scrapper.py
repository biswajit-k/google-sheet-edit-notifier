import requests
import winsound
import time
import os

# variables
sheet_id = os.getenv('SHEET_ID')
scm_url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/"

test_sheet_id = os.getenv('TEST_SHEET_ID')
test_url = f"https://sheets.googleapis.com/v4/spreadsheets/{test_sheet_id}/"

# url settings
url = test_url

# sound settings
frequency = 2000
duration = 1500
beep_times = 5

def make_sound(times=1):
    for i in range(times):
        winsound.Beep(frequency, duration)
        time.sleep(1)


# config variables
from dotenv import load_dotenv
load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIEND_SECRET = os.getenv('CLIENT_SECRET')
REFRESH_TOKEN = os.getenv('REFRESH_TOKEN')


# helper functions
def get_access_token(client_id, client_secret, refresh_token):
    import requests

    params = {
            "grant_type": "refresh_token",
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": refresh_token
    }

    authorization_url = "https://oauth2.googleapis.com/token"

    r = requests.post(authorization_url, data=params)

    if r.ok:
            return r.json()['access_token']
    else:
            return None


def get_cell_values(url):
    url += 'values:batchGet'

    params = {
        'ranges': 'sheet1!A1:ZZ150',
    }

    access_token = get_access_token(CLIENT_ID, CLIEND_SECRET, REFRESH_TOKEN)
    headers = {"Authorization": "Bearer " + access_token }

    r = requests.get(url, headers=headers, params=params)
    if r.ok:
        return r.json()

    raise Exception(f"Error in request-\n\n{r.text}")


def get_filled_cell_count(url):

    cell_values_response = get_cell_values(url)

    rows = cell_values_response['valueRanges'][0]['values']

    count = 0
    for row in rows:
        count += sum(1 for value in row if value != '')

    return count


# code
filled_cell_count = -1

while True:
    print("Checking....")

    try:
        current_filled_cell_count = get_filled_cell_count(url)
    except KeyboardInterrupt:
        import sys
        sys.exit()
    except:
        make_sound()
        print("Oops! Something went wrong retrying!...")
        continue

    if filled_cell_count == -1:
        filled_cell_count = current_filled_cell_count

    elif filled_cell_count != current_filled_cell_count:            # count changed => edit done
        print(f"Found. Playing beep sound {beep_times} times")
        make_sound(beep_times)

    print("Not Found. Sleeping....")
    time.sleep(5)
