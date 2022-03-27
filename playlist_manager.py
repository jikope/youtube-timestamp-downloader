#!/usr/bin/python3
import downloader
import json
import google_sheet
import sys

download_dir = '/media/data/bima/lagu/Gamelan/Yogyakarta/'
sheet_url = "https://spreadsheets.google.com/feeds/list/1R1IGG3ETEWHxhWxIuFCfkGwOZUy3W4syATL6RzQrURc/1/public/values?alt=json"

def read_playlist():
    """Read tracks from playlist file(json)"""
    with open('playlist.json', 'r') as playlist_json:
        playlist = json.loads(playlist_json.read())

        return playlist

def get_undownloaded_track(playlist):
    undownloaded_tracks = [track for track in playlist if track['downloaded'] == False]

    return undownloaded_tracks

def sync_playlist(tracks):
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


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print_message()
        print("\nExiting program ...")
        quit()

    if sys.argv[1] == 'update':
        google_sheet.update(sheet_url)
    elif sys.argv[1] == 'sync':
        playlist = read_playlist()
        undownloaded_tracks = get_undownloaded_track(playlist)
        sync_playlist(undownloaded_tracks)
    else:
        print_message()

        
