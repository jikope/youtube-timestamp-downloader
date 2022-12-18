#!/usr/bin/python3
import urllib.request, json 
import subprocess

def get_json(sheet_url):
    """ Get data from Google Sheet"""
    with urllib.request.urlopen(sheet_url) as url:
        raw_data = json.loads(url.read().decode())
        data = []
        #rows = raw_data['feed']['entry']
        rows = raw_data['values']
        heading = rows.pop(0) # Remove heading

        for row in rows:
            formattedRow = {} # row for each track
            formattedRow['gendhing'] = row[0].replace("\n", " ")
            formattedRow['laras'] = row[1]
            formattedRow['url'] = row[2]
            formattedRow['start'] = row[3]
            formattedRow['end'] = row[4]
            formattedRow['duration'] = row[5]
            formattedRow['gangsa'] = row[6]
            formattedRow['downloaded'] = False
            data.append(formattedRow)

        return data
    
def check_file_downloaded(raw_playlist_data, playlist_dir):
    """Check if track already downloaded"""
    cmd = "ls " + playlist_dir
    out = subprocess.run(cmd.split(), stdout=subprocess.PIPE)
    downloaded_track_filename = out.stdout.decode().replace('.mp3', '').split('\n')

    playlist_data = []
    undownload_count = 0

    for track in raw_playlist_data:
        if track['gendhing'] in downloaded_track_filename:
            track['downloaded'] = True
        else: 
            undownload_count += 1

        playlist_data.append(track)

    if undownload_count != 0:
        print(str(undownload_count) + " undownloaded track detected")
    else:
        print("Playlist is up to date")

    return playlist_data

def write_json_file(playlist_dict):
    "Save playlist as json file"
    json_export = json.dumps(playlist_dict, indent=4)

    with open("playlist.json", 'w') as outfile:
        outfile.write(json_export)


API_KEY = "YOUR_API_KEY"
DOWNLOAD_DIR = "/media/data/bima/lagu/Gamelan/Yogyakarta/"
SHEET_URL = "https://sheets.googleapis.com/v4/spreadsheets/1R1IGG3ETEWHxhWxIuFCfkGwOZUy3W4syATL6RzQrURc/values/Sheet1"

if __name__ == "__main__":
    raw_playlist_data = get_json(SHEET_URL + API_KEY)
    playlist_data = check_file_downloaded(raw_playlist_data, '/media/data/bima/lagu/Gamelan/Yogyakarta/')
    write_json_file(playlist_data)
