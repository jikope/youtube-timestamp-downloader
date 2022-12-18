#!/usr/bin/python3
import downloader
import json
import google_sheet
import sys

# download_dir = '/media/data/bima/lagu/Gamelan/Yogyakarta/'
# sheet_url = "https://spreadsheets.google.com/feeds/list/1R1IGG3ETEWHxhWxIuFCfkGwOZUy3W4syATL6RzQrURc/1/public/values?alt=json"
API_KEY = "?key=AIzaSyBKEJXqjIpOvhH-15cwli2UZZrj4inrj90"
SHEET_URL = "https://sheets.googleapis.com/v4/spreadsheets/1R1IGG3ETEWHxhWxIuFCfkGwOZUy3W4syATL6RzQrURc/values/Sheet1"
DOWNLOAD_DIR = "/media/data/bima/lagu/Gamelan/Yogyakarta/"

def read_playlist():
    """Read tracks from playlist file(json)"""
    with open('playlist.json', 'r') as playlist_json:
        playlist = json.loads(playlist_json.read())

        return playlist

def get_undownloaded_track(playlist):
    undownloaded_tracks = [track for track in playlist if track['downloaded'] == False]

    return undownloaded_tracks

def sync_playlist(tracks, download_dir):
    """Queue download tracks"""
    for i in range(0, len(tracks)):
        print(str(i) + " of " + str(len(tracks)))
        audio_track = downloader.get_audio_track(tracks[i]['url'])
        download = downloader.download_audio_parts(audio_track, tracks[i], download_dir)
        tracks[i]['downloaded'] = True
        google_sheet.write_json_file(tracks)


def print_message():
    print("Please enter available command")
    print("\tupdate = update playlist items")
    print("\tsync = download playlist to mp3 file")


def main():
    if len(sys.argv) == 1:
        print_message()
        print("\nExiting program ...")
        quit()

    if sys.argv[1] == 'update':
        raw_playlist_data = google_sheet.get_json(SHEET_URL + API_KEY)
        playlist_data = google_sheet.check_file_downloaded(raw_playlist_data, DOWNLOAD_DIR)
        google_sheet.write_json_file(playlist_data)
        # google_sheet.update(SHEET_URL + API_KEY, DOWNLOAD_DIR)
    elif sys.argv[1] == 'sync':
        playlist = read_playlist()
        undownloaded_tracks = get_undownloaded_track(playlist)
        sync_playlist(undownloaded_tracks, DOWNLOAD_DIR)
    else:
        print_message()

if __name__ == '__main__':
    main()
