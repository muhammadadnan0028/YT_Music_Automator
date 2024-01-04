import requests,json,time,random
from uiautomator2 import Device


def fetch_songs_from_spreadsheet():
    SPREADSHEET_ID = "1u0IRlcGf1xfCm9GvWFjEMC4SRRyAX4BOslK6WYUnvJA"
    SHEET_TITLE = "Feuille"
    SHEET_RANGE = "A1:C20"
    print("[+] Fetching songs from Google Spreadsheet")
    full_url = f'https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?sheet={SHEET_TITLE}&range={SHEET_RANGE}'
    
    response = requests.get(full_url)
    data = response.text[47:-2]
    parsed_data = json.loads(data)
    
    rows = []
    table_rows = parsed_data['table']['rows']
    for row in table_rows:
        try:
            # Assuming the values are directly under 'v' key
            values_in_row = [cell['v'] for cell in row['c']]
            rows.append(values_in_row)
        except KeyError as e:
            # Print rows causing issues for debugging
            print(f"KeyError: {e} - Row: {row}")  
    return rows

########################################################################################################################################
########################################################################################################################################


def random_click(device):
    time.sleep(6)
    skip = device.xpath('//*[@resource-id="com.google.android.apps.youtube.music:id/skip_ad_button"]/android.widget.LinearLayout[1]')
    if skip.exists:
        skip.click()
    back_button = device.xpath('//*[@resource-id="com.google.android.apps.youtube.music:id/player_collapse_button"]')
    back_button.click()
    time.sleep(3)

    samples_tab= device.xpath('//*[@text="Samples"]')
    samples_tab.click()
    time.sleep(0.2)
    samples_tab.click()
    device.swipe_ext("up", 0.5)
    time.sleep(3)
    explore= device.xpath('//*[@text="Explore"]')
    explore.click()
    time.sleep(0.2)
    explore.click()
    device.swipe_ext("up", 0.5)
    time.sleep(2)
    device.swipe_ext("down", 0.5)
    

########################################################################################################################################
########################################################################################################################################


def play_youtube_music_manually(song_title,artist,device):
    device.session("com.google.android.apps.youtube.music")
    time.sleep(4)
    search_icon = device.xpath('//*[@resource-id="com.google.android.apps.youtube.music:id/action_search_button"]')
    search_icon.click()
    time.sleep(3)
    search_bar= device.xpath('//*[@resource-id="com.google.android.apps.youtube.music:id/search_edit_text"]')
    search_bar.set_text(f"{song_title} {artist}")
    time.sleep(4)
    device.press("enter")
    time.sleep(3)
    first_result = device.xpath('//*[@resource-id="com.google.android.apps.youtube.music:id/first_entity_button_container"]')
    first_result.click()
    random_click(device)


########################################################################################################################################
########################################################################################################################################


def play_youtube_music_deepLink(video_url, device):
    # Launch YouTube Music with the given video URL
    device._adb_shell(f"am start -a android.intent.action.VIEW -d '{video_url}' com.google.android.apps.youtube.music")
    time.sleep(4)

    # Minimize the player interface
    random_click(device)


########################################################################################################################################
########################################################################################################################################


def randomize(device):
    songs = fetch_songs_from_spreadsheet()
    for song_info in songs[1:]:
        song_title, artist, video_url = song_info
        options = [0, 1]
        random_number = random.choice(options)
        if random_number == 0:
            print(f"[+] Playing {song_title} by {artist} (manual)")
            play_youtube_music_manually(song_title,artist,device)
            time.sleep(3)
        else:
            print(f"[+] Playing {song_title} by {artist} (deeplink)")
            play_youtube_music_deepLink(video_url, device)
            time.sleep(3)
        time.sleep(30)
        

########################################################################################################################################
########################################################################################################################################


def main():
    device = Device("emulator-5554")
    randomize(device)


if __name__ == "__main__":
    main()
