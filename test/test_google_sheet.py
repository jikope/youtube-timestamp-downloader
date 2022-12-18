import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")

from google_sheet import get_json

API_KEY = "YOUR_API_KEY"
SHEET_URL = "https://sheets.googleapis.com/v4/spreadsheets/1R1IGG3ETEWHxhWxIuFCfkGwOZUy3W4syATL6RzQrURc/values/Sheet1"

def test_get_json():
    raw_playlist_data = get_json(SHEET_URL + API_KEY)
    assert raw_playlist_data == 0
