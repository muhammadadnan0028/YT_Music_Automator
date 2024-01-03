import requests
import json
import time
from uiautomator2 import Device

SPREADSHEET_ID = "1u0IRlcGf1xfCm9GvWFjEMC4SRRyAX4BOslK6WYUnvJA"
SHEET_TITLE = "Feuille"
SHEET_RANGE = "A1:C20"

def fetch_songs_from_spreadsheet():
    print("[+] Fetching songs from Google Spreadsheet")
    full_url = f'https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?sheet={SHEET_TITLE}&range={SHEET_RANGE}'
    
    response = requests.get(full_url)
    data = response.text[47:-2]
    parsed_data = json.loads(data)
    
    rows = []
    table_rows = parsed_data['table']['rows']
    for row in table_rows:
        try:
            values_in_row = [cell['v'] for cell in row['c']]  # Assuming the values are directly under 'v' key
            rows.append(values_in_row)
        except KeyError as e:
            print(f"KeyError: {e} - Row: {row}")  # Print rows causing issues for debugging
    
    return rows


def play_youtube_music(video_url, device):
    device._adb_shell(f"am start -a android.intent.action.VIEW -d '{video_url}' com.google.android.apps.youtube.music")
    time.sleep(4)
    skip=device.xpath('//*[@resource-id="com.google.android.apps.youtube.music:id/skip_ad_button"]/android.widget.LinearLayout[1]')
    if skip.exists:
        skip.click()
    back_button = device.xpath('//*[@resource-id="com.google.android.apps.youtube.music:id/player_collapse_button"]')
    back_button.click()
    device.swipe_ext("up", 0.5)
    time.sleep(30)

def main():
    device = Device("emulator-5554")
    songs = fetch_songs_from_spreadsheet()
    while True:
        for song_info in songs[1:]:
            song_title, artist, video_url = song_info
            print(f"[+] Playing {song_title} by {artist}")
            play_youtube_music(video_url, device)
            time.sleep(3)

if __name__ == "__main__":
    main()
