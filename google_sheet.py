#!/usr/bin/python3
import urllib.request, json 
import subprocess

def get_json(sheet_url):
    """ Get data from Google Sheet"""
    with urllib.request.urlopen(sheet_url) as url:
        raw_data = json.loads(url.read().decode())
        data = []
        rows = raw_data['feed']['entry']

        for row in rows:
            formattedRow = {} # row for each track
            for key in row:
                if(key.startswith("gsx$")):
                    formattedRow[key.replace("gsx$", "")] = row[key]['$t'].replace("\n", " ")

            formattedRow['downloaded'] = False
            data.append(formattedRow)
    
        return data
        
    
def check_file_downloaded(raw_playlist_data, playlist_dir):
    """Function to check if track already downloaded"""
    cmd = "ls " + playlist_dir
    out = subprocess.run(cmd.split(), stdout=subprocess.PIPE)
    downloaded_track_filename = out.stdout.decode().replace('.mp3', '').split('\n')

    playlist_data = []
    undownload_count = 0

    for track in raw_playlist_data:
        #print(track['gendhing'] in downloaded_track_filename)
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
    json_export = json.dumps(playlist_dict, indent=4)

    with open("playlist.json", 'w') as outfile:
        outfile.write(json_export)

def update(sheet_url):
    raw_playlist_data = get_json(sheet_url)
    playlist_data = check_file_downloaded(raw_playlist_data, '/media/data/bima/lagu/Gamelan/Yogyakarta/')
    write_json_file(playlist_data)

if __name__ == "__main__":
    raw_playlist_data = get_json('https://spreadsheets.google.com/feeds/list/1R1IGG3ETEWHxhWxIuFCfkGwOZUy3W4syATL6RzQrURc/1/public/values?alt=json')
    playlist_data = check_file_downloaded(raw_playlist_data, '/media/data/bima/lagu/Gamelan/Yogyakarta/')
    write_json_file(playlist_data)

